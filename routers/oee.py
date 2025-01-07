from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.oee import OEECreate, OEEOut
from schemas.count_type import CountTypeCreate, CountTypeUpdate, CountTypeOut
from schemas.count_tag import CountTagCreate, CountTagOut
from schemas.count_history import CountHistoryCreate, CountHistoryOut
from database.models.oee import OEE, CountType, CountTag, CountHistory
from utils.dependencies import get_db

router = APIRouter(
    prefix="/oee",
    tags=["OEE"]
)

# CountType CRUD
@router.post("/count-type/", response_model=CountTypeOut, status_code=status.HTTP_201_CREATED)
def create_count_type(count_type_in: CountTypeCreate, db: Session = Depends(get_db)):
    """
    Create a new CountType.
    """
    existing = db.query(CountType).filter(CountType.count_type == count_type_in.count_type).first()
    if existing:
        raise CustomException("CountType already exists.", status_code=status.HTTP_400_BAD_REQUEST)
    new_count_type = CountType(**count_type_in.dict())
    db.add(new_count_type)
    db.commit()
    db.refresh(new_count_type)
    return new_count_type

@router.get("/count-type/", response_model=List[CountTypeOut])
def get_all_count_types(db: Session = Depends(get_db)):
    """
    Retrieve all CountTypes.
    """
    return db.query(CountType).all()

@router.put("/count-type/{count_type_id}", response_model=CountTypeOut)
def update_count_type(count_type_id: int, count_type_upd: CountTypeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing CountType.
    """
    count_type = db.query(CountType).get(count_type_id)
    if not count_type:
        raise HTTPException(status_code=404, detail="CountType not found.")
    for key, value in count_type_upd.dict(exclude_unset=True).items():
        setattr(count_type, key, value)
    db.commit()
    db.refresh(count_type)
    return count_type

@router.delete("/count-type/{count_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_count_type(count_type_id: int, db: Session = Depends(get_db)):
    """
    Delete a CountType.
    """
    count_type = db.query(CountType).get(count_type_id)
    if not count_type:
        raise HTTPException(status_code=404, detail="CountType not found.")
    db.delete(count_type)
    db.commit()

# CountTag CRUD
@router.post("/count-tag/", response_model=CountTagOut, status_code=status.HTTP_201_CREATED)
def create_count_tag(count_tag_in: CountTagCreate, db: Session = Depends(get_db)):
    """
    Create a new CountTag.
    """
    new_count_tag = CountTag(**count_tag_in.dict())
    db.add(new_count_tag)
    db.commit()
    db.refresh(new_count_tag)
    return new_count_tag

@router.get("/count-tag/", response_model=List[CountTagOut])
def get_all_count_tags(db: Session = Depends(get_db)):
    """
    Retrieve all CountTags.
    """
    return db.query(CountTag).all()

# CountHistory CRUD
@router.post("/count-history/", response_model=CountHistoryOut, status_code=status.HTTP_201_CREATED)
def create_count_history(count_history_in: CountHistoryCreate, db: Session = Depends(get_db)):
    """
    Record a CountHistory.
    """
    # Ensure CountTag and CountType exist
    count_tag = db.query(CountTag).filter(CountTag.id == count_history_in.tag_id).first()
    count_type = db.query(CountType).filter(CountType.id == count_history_in.count_type_id).first()
    if not count_tag or not count_type:
        raise CustomException("Invalid CountTag or CountType.")
    new_count_history = CountHistory(**count_history_in.dict())
    db.add(new_count_history)
    db.commit()
    db.refresh(new_count_history)
    return new_count_history

@router.get("/count-history/", response_model=List[CountHistoryOut])
def get_all_count_histories(db: Session = Depends(get_db)):
    """
    Retrieve all CountHistories.
    """
    return db.query(CountHistory).all()
