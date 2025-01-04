from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.enterprise import SiteCreate, SiteUpdate, SiteOut
from database.models.enterprise import Site, Enterprise
from utils.dependencies import get_db
from auth.dependencies import get_current_user
from utils.exception_handler import CustomException

router = APIRouter(
    prefix="/site",
    tags=["Site"],
    dependencies=[Depends(get_current_user)],  # Protect all endpoints with JWT
)

@router.post("/", response_model=SiteOut, status_code=status.HTTP_201_CREATED)
def create_site(site_in: SiteCreate, db: Session = Depends(get_db)):
    """
    Create a new site.
    """
    # Check if the parent enterprise exists
    parent_enterprise = db.query(Enterprise).filter(Enterprise.id == site_in.enterprise_id).first()
    if not parent_enterprise:
        raise CustomException("Parent enterprise not found.", status_code=status.HTTP_400_BAD_REQUEST)

    new_site = Site(**site_in.dict())
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site

@router.get("/", response_model=List[SiteOut])
def get_all_sites(db: Session = Depends(get_db)):
    """
    Retrieve all sites.
    """
    return db.query(Site).all()

@router.get("/{site_id}", response_model=SiteOut)
def get_site(site_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific site by ID.
    """
    site = db.query(Site).get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found.")
    return site

@router.put("/{site_id}", response_model=SiteOut)
def update_site(site_id: int, site_upd: SiteUpdate, db: Session = Depends(get_db)):
    """
    Update an existing site.
    """
    site = db.query(Site).get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found.")

    for key, value in site_upd.dict(exclude_unset=True).items():
        setattr(site, key, value)
    db.commit()
    db.refresh(site)
    return site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    """
    Delete a site.
    """
    site = db.query(Site).get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found.")
    db.delete(site)
    db.commit()