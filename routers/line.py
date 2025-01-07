"""
Router for handling Line-related operations in the MES system.
Lines are production units within Areas, containing Cells.
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.enterprise import LineCreate, LineUpdate, LineOut
from database.models.enterprise import Line, Area
from utils.dependencies import get_db
from utils.logging_utils import (
    log_endpoint_access,
    log_entity_not_found,
    log_duplicate_entity,
    log_query_result
)

router = APIRouter(
    prefix="/line",
    tags=["Line"]
)

@router.post("/", response_model=LineOut, status_code=status.HTTP_201_CREATED)
def create_line(line_in: LineCreate, db: Session = Depends(get_db)):
    """
    Create a new production line within an area.
    """
    # Validate parent area exists
    area = db.query(Area).filter(Area.id == line_in.parent_id).first()
    if not area:
        log_entity_not_found("Area", f"id={line_in.parent_id}")
        raise HTTPException(status_code=404, detail="Parent area not found")

    # Check for duplicate line name within the area
    existing = db.query(Line).filter(
        Line.name == line_in.name,
        Line.area_id == line_in.parent_id
    ).first()
    if existing:
        log_duplicate_entity("Line", f"name='{line_in.name}' in area_id={line_in.parent_id}")
        raise HTTPException(status_code=400, detail="Line with this name already exists in the area")

    new_line = Line(
        name=line_in.name,
        area_id=line_in.parent_id,
        disabled=line_in.disabled,
        timestamp=datetime.utcnow()
    )
    db.add(new_line)
    db.commit()
    db.refresh(new_line)
    log_endpoint_access("Line", "created", f"name='{new_line.name}' in area='{area.name}'")
    return new_line

@router.get("/", response_model=List[LineOut])
def get_all_lines(db: Session = Depends(get_db)):
    """
    Retrieve all production lines.
    """
    lines = db.query(Line).all()
    log_query_result("Line", len(lines))
    return lines

@router.get("/{line_id}", response_model=LineOut)
def get_line(line_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific production line by ID.
    """
    line = db.query(Line).filter(Line.id == line_id).first()
    if not line:
        log_entity_not_found("Line", f"id={line_id}")
        raise HTTPException(status_code=404, detail="Line not found")
    log_endpoint_access("Line", "retrieved", f"name='{line.name}'")
    return line

@router.put("/{line_id}", response_model=LineOut)
def update_line(line_id: int, line_upd: LineUpdate, db: Session = Depends(get_db)):
    """
    Update an existing production line.
    """
    line = db.query(Line).filter(Line.id == line_id).first()
    if not line:
        log_entity_not_found("Line", f"id={line_id}")
        raise HTTPException(status_code=404, detail="Line not found")

    # If updating parent_id, validate new parent exists
    if line_upd.parent_id is not None:
        area = db.query(Area).filter(Area.id == line_upd.parent_id).first()
        if not area:
            log_entity_not_found("Area", f"id={line_upd.parent_id}")
            raise HTTPException(status_code=404, detail="New parent area not found")

    update_data = line_upd.dict(exclude_unset=True)
    if 'parent_id' in update_data:
        update_data['area_id'] = update_data.pop('parent_id')

    for field, value in update_data.items():
        setattr(line, field, value)
    
    db.commit()
    db.refresh(line)
    log_endpoint_access("Line", "updated", f"name='{line.name}'")
    return line

@router.delete("/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_line(line_id: int, db: Session = Depends(get_db)):
    """
    Delete a production line.
    """
    line = db.query(Line).filter(Line.id == line_id).first()
    if not line:
        log_entity_not_found("Line", f"id={line_id}")
        raise HTTPException(status_code=404, detail="Line not found")
    
    name = line.name  # Store name before deletion
    db.delete(line)
    db.commit()
    log_endpoint_access("Line", "deleted", f"name='{name}'")
    return None
