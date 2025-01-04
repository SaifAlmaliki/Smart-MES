# file: app/routers/cell.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.enterprise import CellCreate, CellUpdate, CellOut
from database.models.enterprise import Cell, Line
from utils.dependencies import get_db
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/cell",
    tags=["Cell"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=CellOut, status_code=status.HTTP_201_CREATED)
def create_cell(cell_in: CellCreate, db: Session = Depends(get_db)):
    """
    Create a new cell.
    """
    # Check if the parent line exists
    parent_line = db.query(Line).filter(Line.id == cell_in.line_id).first()
    if not parent_line:
        raise HTTPException(status_code=400, detail="Parent line not found.")

    new_cell = Cell(**cell_in.dict())
    db.add(new_cell)
    db.commit()
    db.refresh(new_cell)
    return new_cell

@router.get("/", response_model=List[CellOut])
def get_all_cells(db: Session = Depends(get_db)):
    """
    Retrieve all cells.
    """
    return db.query(Cell).all()

@router.get("/{cell_id}", response_model=CellOut)
def get_cell(cell_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific cell by ID.
    """
    cell = db.query(Cell).get(cell_id)
    if not cell:
        raise HTTPException(status_code=404, detail="Cell not found.")
    return cell

@router.put("/{cell_id}", response_model=CellOut)
def update_cell(cell_id: int, cell_upd: CellUpdate, db: Session = Depends(get_db)):
    """
    Update an existing cell.
    """
    cell = db.query(Cell).get(cell_id)
    if not cell:
        raise HTTPException(status_code=404, detail="Cell not found.")

    for key, value in cell_upd.dict(exclude_unset=True).items():
        setattr(cell, key, value)
    db.commit()
    db.refresh(cell)
    return cell

@router.delete("/{cell_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cell(cell_id: int, db: Session = Depends(get_db)):
    """
    Delete a cell (soft-delete recommended in production).
    """
    cell = db.query(Cell).get(cell_id)
    if not cell:
        raise HTTPException(status_code=404, detail="Cell not found.")
    db.delete(cell)
    db.commit()
