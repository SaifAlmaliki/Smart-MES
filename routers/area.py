from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.enterprise import AreaCreate, AreaUpdate, AreaOut
from database.models.enterprise import Area, Site
from utils.dependencies import get_db

router = APIRouter(
    prefix="/area",
    tags=["Area"]
)

@router.post("/", response_model=AreaOut, status_code=status.HTTP_201_CREATED)
def create_area(area_in: AreaCreate, db: Session = Depends(get_db)):
    """
    Create a new area.
    """
    # Validate parent site exists
    site = db.query(Site).filter(Site.id == area_in.parent_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Parent site not found")

    new_area = Area(**area_in.dict())
    db.add(new_area)
    db.commit()
    db.refresh(new_area)
    return new_area

@router.get("/", response_model=List[AreaOut])
def get_all_areas(db: Session = Depends(get_db)):
    """
    Retrieve all areas.
    """
    return db.query(Area).all()

@router.get("/{area_id}", response_model=AreaOut)
def get_area(area_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific area by ID.
    """
    area = db.query(Area).get(area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found.")
    return area

@router.put("/{area_id}", response_model=AreaOut)
def update_area(area_id: int, area_upd: AreaUpdate, db: Session = Depends(get_db)):
    """
    Update an existing area.
    """
    area = db.query(Area).get(area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found.")

    for key, value in area_upd.dict(exclude_unset=True).items():
        setattr(area, key, value)
    db.commit()
    db.refresh(area)
    return area

@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area(area_id: int, db: Session = Depends(get_db)):
    """
    Delete an area (soft-delete recommended in production).
    """
    area = db.query(Area).get(area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found.")
    db.delete(area)
    db.commit()
