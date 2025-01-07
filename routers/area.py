"""
Router for handling Area-related operations in the MES system.
Areas are organizational units within Sites, containing production Lines.
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.enterprise import AreaCreate, AreaUpdate, AreaOut
from database.models.enterprise import Area, Site
from utils.dependencies import get_db
from utils.logging_utils import (
    log_endpoint_access,
    log_entity_not_found,
    log_duplicate_entity,
    log_query_result
)

router = APIRouter(
    prefix="/area",
    tags=["Area"]
)

@router.post("/", response_model=AreaOut, status_code=status.HTTP_201_CREATED)
def create_area(area_in: AreaCreate, db: Session = Depends(get_db)):
    """
    Create a new area within a site.
    """
    # Validate parent site exists
    site = db.query(Site).filter(Site.id == area_in.parent_id).first()
    if not site:
        log_entity_not_found("Site", f"id={area_in.parent_id}")
        raise HTTPException(status_code=404, detail="Parent site not found")

    # Check for duplicate area name within the site
    existing = db.query(Area).filter(
        Area.name == area_in.name,
        Area.site_id == area_in.parent_id
    ).first()
    if existing:
        log_duplicate_entity("Area", f"name='{area_in.name}' in site_id={area_in.parent_id}")
        raise HTTPException(status_code=400, detail="Area with this name already exists in the site")

    new_area = Area(
        name=area_in.name,
        site_id=area_in.parent_id,
        disabled=area_in.disabled,
        timestamp=datetime.utcnow()
    )
    db.add(new_area)
    db.commit()
    db.refresh(new_area)
    log_endpoint_access("Area", "created", f"name='{new_area.name}' in site='{site.name}'")
    return new_area

@router.get("/", response_model=List[AreaOut])
def get_all_areas(db: Session = Depends(get_db)):
    """
    Retrieve all areas.
    """
    areas = db.query(Area).all()
    log_query_result("Area", len(areas))
    return areas

@router.get("/{area_id}", response_model=AreaOut)
def get_area(area_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific area by ID.
    """
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        log_entity_not_found("Area", f"id={area_id}")
        raise HTTPException(status_code=404, detail="Area not found")
    log_endpoint_access("Area", "retrieved", f"name='{area.name}'")
    return area

@router.put("/{area_id}", response_model=AreaOut)
def update_area(area_id: int, area_upd: AreaUpdate, db: Session = Depends(get_db)):
    """
    Update an existing area.
    """
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        log_entity_not_found("Area", f"id={area_id}")
        raise HTTPException(status_code=404, detail="Area not found")

    # If updating parent_id, validate new parent exists
    if area_upd.parent_id is not None:
        site = db.query(Site).filter(Site.id == area_upd.parent_id).first()
        if not site:
            log_entity_not_found("Site", f"id={area_upd.parent_id}")
            raise HTTPException(status_code=404, detail="New parent site not found")

    update_data = area_upd.dict(exclude_unset=True)
    if 'parent_id' in update_data:
        update_data['site_id'] = update_data.pop('parent_id')

    for field, value in update_data.items():
        setattr(area, field, value)
    
    db.commit()
    db.refresh(area)
    log_endpoint_access("Area", "updated", f"name='{area.name}'")
    return area

@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area(area_id: int, db: Session = Depends(get_db)):
    """
    Delete an area.
    """
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        log_entity_not_found("Area", f"id={area_id}")
        raise HTTPException(status_code=404, detail="Area not found")
    
    name = area.name  # Store name before deletion
    db.delete(area)
    db.commit()
    log_endpoint_access("Area", "deleted", f"name='{name}'")
    return None
