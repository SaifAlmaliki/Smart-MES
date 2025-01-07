from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.enterprise import SiteCreate, SiteUpdate, SiteOut
from database.models.enterprise import Site, Enterprise
from utils.dependencies import get_db
from utils.logging_utils import (
    log_endpoint_access,
    log_entity_not_found,
    log_duplicate_entity,
    log_query_result
)

router = APIRouter(
    prefix="/site",
    tags=["Site"]
)

@router.post("/", response_model=SiteOut, status_code=status.HTTP_201_CREATED)
def create_site(site_in: SiteCreate, db: Session = Depends(get_db)):
    """
    Create a new site.
    """
    # Validate parent enterprise exists
    enterprise = db.query(Enterprise).filter(Enterprise.id == site_in.parent_id).first()
    if not enterprise:
        log_entity_not_found("Enterprise", f"id={site_in.parent_id}")
        raise HTTPException(status_code=404, detail="Parent enterprise not found")

    # Check for duplicate site name within the enterprise
    existing = db.query(Site).filter(
        Site.name == site_in.name,
        Site.enterprise_id == site_in.parent_id
    ).first()
    if existing:
        log_duplicate_entity("Site", f"name='{site_in.name}' in enterprise_id={site_in.parent_id}")
        raise HTTPException(status_code=400, detail="Site with this name already exists in the enterprise")

    new_site = Site(
        name=site_in.name,
        enterprise_id=site_in.parent_id,
        disabled=site_in.disabled,
        timestamp=datetime.utcnow()
    )
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    log_endpoint_access("Site", "created", f"name='{new_site.name}' in enterprise='{enterprise.name}'")
    return new_site

@router.get("/", response_model=List[SiteOut])
def get_all_sites(db: Session = Depends(get_db)):
    """
    Retrieve all sites.
    """
    sites = db.query(Site).all()
    log_query_result("Site", len(sites))
    return sites

@router.get("/{site_id}", response_model=SiteOut)
def get_site(site_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific site by ID.
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        log_entity_not_found("Site", f"id={site_id}")
        raise HTTPException(status_code=404, detail="Site not found")
    log_endpoint_access("Site", "retrieved", f"name='{site.name}'")
    return site

@router.put("/{site_id}", response_model=SiteOut)
def update_site(site_id: int, site_upd: SiteUpdate, db: Session = Depends(get_db)):
    """
    Update an existing site.
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        log_entity_not_found("Site", f"id={site_id}")
        raise HTTPException(status_code=404, detail="Site not found")

    # If updating parent_id, validate new parent exists
    if site_upd.parent_id is not None:
        enterprise = db.query(Enterprise).filter(Enterprise.id == site_upd.parent_id).first()
        if not enterprise:
            log_entity_not_found("Enterprise", f"id={site_upd.parent_id}")
            raise HTTPException(status_code=404, detail="New parent enterprise not found")
        site_upd.enterprise_id = site_upd.parent_id

    update_data = site_upd.dict(exclude_unset=True)
    if 'parent_id' in update_data:
        update_data['enterprise_id'] = update_data.pop('parent_id')

    for field, value in update_data.items():
        setattr(site, field, value)
    
    db.commit()
    db.refresh(site)
    log_endpoint_access("Site", "updated", f"name='{site.name}'")
    return site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    """
    Delete a site.
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        log_entity_not_found("Site", f"id={site_id}")
        raise HTTPException(status_code=404, detail="Site not found")
    
    name = site.name  # Store name before deletion
    db.delete(site)
    db.commit()
    log_endpoint_access("Site", "deleted", f"name='{name}'")
    return None
