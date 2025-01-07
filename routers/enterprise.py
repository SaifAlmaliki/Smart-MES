from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from schemas.enterprise import EnterpriseCreate, EnterpriseUpdate, EnterpriseOut
from database.models.enterprise import Enterprise
from utils.dependencies import get_db
from utils.logging_utils import (
    log_endpoint_access,
    log_entity_not_found,
    log_duplicate_entity,
    log_query_result
)

router = APIRouter(
    prefix="/enterprise",
    tags=["Enterprise"]
)

@router.post("/", response_model=EnterpriseOut, status_code=status.HTTP_201_CREATED)
def create_enterprise(
    enterprise_in: EnterpriseCreate, db: Session = Depends(get_db)
):
    """
    Create a new enterprise.
    """
    existing = db.query(Enterprise).filter(Enterprise.name == enterprise_in.name).first()
    if existing:
        log_duplicate_entity("Enterprise", f"name='{enterprise_in.name}'")
        raise HTTPException(status_code=400, detail="Enterprise already exists.")

    new_ent = Enterprise(
        name=enterprise_in.name,
        disabled=enterprise_in.disabled,
        timestamp=datetime.utcnow()
    )
    db.add(new_ent)
    db.commit()
    db.refresh(new_ent)
    log_endpoint_access("Enterprise", "created", f"name='{new_ent.name}'")
    return new_ent

@router.get("/", response_model=List[EnterpriseOut])
def get_all_enterprises(db: Session = Depends(get_db)):
    """
    Retrieve all enterprises.
    """
    enterprises = db.query(Enterprise).all()
    log_query_result("Enterprise", len(enterprises))
    return enterprises

@router.get("/{enterprise_id}", response_model=EnterpriseOut)
def get_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific enterprise by ID.
    """
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        log_entity_not_found("Enterprise", f"id={enterprise_id}")
        raise HTTPException(status_code=404, detail="Enterprise not found")
    log_endpoint_access("Enterprise", "retrieved", f"name='{enterprise.name}'")
    return enterprise

@router.put("/{enterprise_id}", response_model=EnterpriseOut)
def update_enterprise(
    enterprise_id: int, enterprise_upd: EnterpriseUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing enterprise.
    """
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        log_entity_not_found("Enterprise", f"id={enterprise_id}")
        raise HTTPException(status_code=404, detail="Enterprise not found")

    for field, value in enterprise_upd.dict(exclude_unset=True).items():
        setattr(enterprise, field, value)
    
    db.commit()
    db.refresh(enterprise)
    log_endpoint_access("Enterprise", "updated", f"name='{enterprise.name}'")
    return enterprise

@router.delete("/{enterprise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """
    Delete an enterprise (soft-delete recommended in production).
    """
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        log_entity_not_found("Enterprise", f"id={enterprise_id}")
        raise HTTPException(status_code=404, detail="Enterprise not found")
    
    name = enterprise.name  # Store name before deletion
    db.delete(enterprise)
    db.commit()
    log_endpoint_access("Enterprise", "deleted", f"name='{name}'")
    return None
