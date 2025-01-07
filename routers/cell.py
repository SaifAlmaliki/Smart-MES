"""
Router for handling Cell-related operations in the MES system.
Cells are the smallest production units, contained within Lines.
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.enterprise import CellCreate, CellUpdate, CellOut
from database.models.enterprise import Cell, Line
from utils.dependencies import get_db
from utils.logging_utils import (
    log_endpoint_access,
    log_entity_not_found,
    log_duplicate_entity,
    log_query_result
)

router = APIRouter(
    prefix="/cell",
    tags=["Cell"]
)

@router.post("/", response_model=CellOut, status_code=status.HTTP_201_CREATED)
def create_cell(cell_in: CellCreate, db: Session = Depends(get_db)):
    """
    Create a new cell within a production line.
    """
    # Validate parent line exists
    line = db.query(Line).filter(Line.id == cell_in.parent_id).first()
    if not line:
        log_entity_not_found("Line", f"id={cell_in.parent_id}")
        raise HTTPException(status_code=404, detail="Parent line not found")

    # Check for duplicate cell name within the line
    existing = db.query(Cell).filter(
        Cell.name == cell_in.name,
        Cell.line_id == cell_in.parent_id
    ).first()
    if existing:
        log_duplicate_entity("Cell", f"name='{cell_in.name}' in line_id={cell_in.parent_id}")
        raise HTTPException(status_code=400, detail="Cell with this name already exists in the line")

    new_cell = Cell(
        name=cell_in.name,
        line_id=cell_in.parent_id,
        disabled=cell_in.disabled,
        timestamp=datetime.utcnow()
    )
    db.add(new_cell)
    db.commit()
    db.refresh(new_cell)
    log_endpoint_access("Cell", "created", f"name='{new_cell.name}' in line='{line.name}'")
    return new_cell

@router.get("/", response_model=List[CellOut])
def get_all_cells(db: Session = Depends(get_db)):
    """
    Retrieve all cells.
    """
    cells = db.query(Cell).all()
    log_query_result("Cell", len(cells))
    return cells

@router.get("/{cell_id}", response_model=CellOut)
def get_cell(cell_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific cell by ID.
    """
    cell = db.query(Cell).filter(Cell.id == cell_id).first()
    if not cell:
        log_entity_not_found("Cell", f"id={cell_id}")
        raise HTTPException(status_code=404, detail="Cell not found")
    log_endpoint_access("Cell", "retrieved", f"name='{cell.name}'")
    return cell

@router.put("/{cell_id}", response_model=CellOut)
def update_cell(cell_id: int, cell_upd: CellUpdate, db: Session = Depends(get_db)):
    """
    Update an existing cell.
    """
    cell = db.query(Cell).filter(Cell.id == cell_id).first()
    if not cell:
        log_entity_not_found("Cell", f"id={cell_id}")
        raise HTTPException(status_code=404, detail="Cell not found")

    # If updating parent_id, validate new parent exists
    if cell_upd.parent_id is not None:
        line = db.query(Line).filter(Line.id == cell_upd.parent_id).first()
        if not line:
            log_entity_not_found("Line", f"id={cell_upd.parent_id}")
            raise HTTPException(status_code=404, detail="New parent line not found")

    update_data = cell_upd.dict(exclude_unset=True)
    if 'parent_id' in update_data:
        update_data['line_id'] = update_data.pop('parent_id')

    for field, value in update_data.items():
        setattr(cell, field, value)
    
    db.commit()
    db.refresh(cell)
    log_endpoint_access("Cell", "updated", f"name='{cell.name}'")
    return cell

@router.delete("/{cell_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cell(cell_id: int, db: Session = Depends(get_db)):
    """
    Delete a cell.
    """
    cell = db.query(Cell).filter(Cell.id == cell_id).first()
    if not cell:
        log_entity_not_found("Cell", f"id={cell_id}")
        raise HTTPException(status_code=404, detail="Cell not found")
    
    name = cell.name  # Store name before deletion
    db.delete(cell)
    db.commit()
    log_endpoint_access("Cell", "deleted", f"name='{name}'")
    return None
