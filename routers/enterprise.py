# file: app/routers/enterprise.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.enterprise import EnterpriseCreate, EnterpriseUpdate, EnterpriseOut
from database.models.enterprise import Enterprise
from utils.dependencies import get_db
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/enterprise",
    tags=["Enterprise"],
    dependencies=[Depends(get_current_user)]  # Protect all endpoints
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
        raise HTTPException(status_code=400, detail="Enterprise already exists.")
    new_ent = Enterprise(**enterprise_in.dict())
    db.add(new_ent)
    db.commit()
    db.refresh(new_ent)
    return new_ent

@router.get("/", response_model=List[EnterpriseOut])
def get_all_enterprises(db: Session = Depends(get_db)):
    """
    Retrieve all enterprises.
    """
    return db.query(Enterprise).all()

@router.get("/{enterprise_id}", response_model=EnterpriseOut)
def get_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific enterprise by ID.
    """
    ent = db.query(Enterprise).get(enterprise_id)
    if not ent:
        raise HTTPException(status_code=404, detail="Enterprise not found.")
    return ent

@router.put("/{enterprise_id}", response_model=EnterpriseOut)
def update_enterprise(
    enterprise_id: int, enterprise_upd: EnterpriseUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing enterprise.
    """
    ent = db.query(Enterprise).get(enterprise_id)
    if not ent:
        raise HTTPException(status_code=404, detail="Enterprise not found.")
    for key, value in enterprise_upd.dict(exclude_unset=True).items():
        setattr(ent, key, value)
    db.commit()
    db.refresh(ent)
    return ent

@router.delete("/{enterprise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """
    Delete an enterprise (soft-delete recommended in production).
    """
    ent = db.query(Enterprise).get(enterprise_id)
    if not ent:
        raise HTTPException(status_code=404, detail="Enterprise not found.")
    db.delete(ent)
    db.commit()
