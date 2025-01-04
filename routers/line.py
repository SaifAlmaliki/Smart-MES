# file: app/routers/line.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.enterprise import LineCreate, LineUpdate, LineOut
from database.models.enterprise import Line, Area
from utils.dependencies import get_db
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/line",
    tags=["Line"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=LineOut, status_code=status.HTTP_201_CREATED)
def create_line(line_in: LineCreate, db: Session = Depends(get_db)):
    """
    Create a new line.
    """
    # Check if the parent area exists
    parent_area = db.query(Area).filter(Area.id == line_in.area_id).first()
    if not parent_area:
        raise HTTPException(status_code=400, detail="Parent area not found.")

    new_line = Line(**line_in.dict())
    db.add(new_line)
    db.commit()
    db.refresh(new_line)
    return new_line

@router.get("/", response_model=List[LineOut])
def get_all_lines(db: Session = Depends(get_db)):
    """
    Retrieve all lines.
    """
    return db.query(Line).all()

@router.get("/{line_id}", response_model=LineOut)
def get_line(line_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific line by ID.
    """
    line = db.query(Line).get(line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found.")
    return line

@router.put("/{line_id}", response_model=LineOut)
def update_line(line_id: int, line_upd: LineUpdate, db: Session = Depends(get_db)):
    """
    Update an existing line.
    """
    line = db.query(Line).get(line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found.")

    for key, value in line_upd.dict(exclude_unset=True).items():
        setattr(line, key, value)
    db.commit()
    db.refresh(line)
    return line

@router.delete("/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_line(line_id: int, db: Session = Depends(get_db)):
    """
    Delete a line (soft-delete recommended in production).
    """
    line = db.query(Line).get(line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found.")
    db.delete(line)
    db.commit()
