from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.oee import OEECreate, OEEOut
from schemas.count_type import CountTypeCreate, CountTypeUpdate, CountTypeOut
from schemas.count_tag import CountTagCreate, CountTagOut
from schemas.count_history import CountHistoryCreate, CountHistoryOut
from database.models.oee import OEE, CountType, CountTag, CountHistory
from utils.dependencies import get_db
from utils.logging_utils import (
    log_endpoint_access,
    log_entity_not_found,
    log_duplicate_entity,
    log_query_result
)

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
        log_duplicate_entity("CountType", f"type='{count_type_in.count_type}'")
        raise HTTPException(status_code=400, detail="CountType already exists.")
    new_count_type = CountType(**count_type_in.dict())
    db.add(new_count_type)
    db.commit()
    db.refresh(new_count_type)
    log_endpoint_access("CountType", "created", f"type='{new_count_type.count_type}'")
    return new_count_type

@router.get("/count-type/", response_model=List[CountTypeOut])
def get_all_count_types(db: Session = Depends(get_db)):
    """
    Retrieve all CountTypes.
    """
    count_types = db.query(CountType).all()
    log_query_result("CountType", len(count_types))
    return count_types

@router.put("/count-type/{count_type_id}", response_model=CountTypeOut)
def update_count_type(count_type_id: int, count_type_upd: CountTypeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing CountType.
    """
    count_type = db.query(CountType).get(count_type_id)
    if not count_type:
        log_entity_not_found("CountType", f"id={count_type_id}")
        raise HTTPException(status_code=404, detail="CountType not found.")
    for key, value in count_type_upd.dict(exclude_unset=True).items():
        setattr(count_type, key, value)
    db.commit()
    db.refresh(count_type)
    log_endpoint_access("CountType", "updated", f"id={count_type_id}")
    return count_type

@router.delete("/count-type/{count_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_count_type(count_type_id: int, db: Session = Depends(get_db)):
    """
    Delete a CountType.
    """
    count_type = db.query(CountType).get(count_type_id)
    if not count_type:
        log_entity_not_found("CountType", f"id={count_type_id}")
        raise HTTPException(status_code=404, detail="CountType not found.")
    db.delete(count_type)
    db.commit()
    log_endpoint_access("CountType", "deleted", f"id={count_type_id}")

# CountTag CRUD
@router.post("/count-tag/", response_model=CountTagOut, status_code=status.HTTP_201_CREATED)
def create_count_tag(count_tag_in: CountTagCreate, db: Session = Depends(get_db)):
    """
    Create a new CountTag.
    """
    # Validate parent count type exists
    count_type = db.query(CountType).filter(CountType.id == count_tag_in.parent_id).first()
    if not count_type:
        log_entity_not_found("CountType", f"id={count_tag_in.parent_id}")
        raise HTTPException(status_code=404, detail="Parent count type not found")

    # Check for duplicate tag path
    existing = db.query(CountTag).filter(CountTag.tag_path == count_tag_in.tag_path).first()
    if existing:
        log_duplicate_entity("CountTag", f"path='{count_tag_in.tag_path}'")
        raise HTTPException(status_code=400, detail="Count tag with this path already exists")

    new_count_tag = CountTag(**count_tag_in.dict())
    db.add(new_count_tag)
    db.commit()
    db.refresh(new_count_tag)
    log_endpoint_access("CountTag", "created", f"path='{new_count_tag.tag_path}'")
    return new_count_tag

@router.get("/count-tag/", response_model=List[CountTagOut])
def get_all_count_tags(db: Session = Depends(get_db)):
    """
    Retrieve all CountTags.
    """
    count_tags = db.query(CountTag).all()
    log_query_result("CountTag", len(count_tags))
    return count_tags

# CountHistory CRUD
@router.post("/count-history/", response_model=CountHistoryOut, status_code=status.HTTP_201_CREATED)
def create_count_history(count_history_in: CountHistoryCreate, db: Session = Depends(get_db)):
    """
    Record a CountHistory.
    """
    # Validate count tag exists and matches count type
    count_tag = db.query(CountTag).filter(CountTag.id == count_history_in.tag_id).first()
    count_type = db.query(CountType).filter(CountType.id == count_history_in.count_type_id).first()

    if not count_tag or not count_type:
        log_entity_not_found("CountTag/CountType", f"tag_id={count_history_in.tag_id}, type_id={count_history_in.count_type_id}")
        raise HTTPException(status_code=404, detail="Invalid CountTag or CountType")

    # Ensure the count tag belongs to the specified count type
    if count_tag.parent_id != count_type.id:
        log_entity_not_found("CountTag/CountType", f"Mismatch: tag.parent_id={count_tag.parent_id}, type.id={count_type.id}")
        raise HTTPException(status_code=400, detail="CountTag does not belong to specified CountType")

    new_count_history = CountHistory(**count_history_in.dict())
    db.add(new_count_history)
    db.commit()
    db.refresh(new_count_history)
    log_endpoint_access("CountHistory", "created", 
                       f"count={new_count_history.count}, tag='{count_tag.tag_path}', type='{count_type.count_type}'")
    return new_count_history

@router.get("/count-history/", response_model=List[CountHistoryOut])
def get_all_count_histories(db: Session = Depends(get_db)):
    """
    Retrieve all CountHistories.
    """
    count_history = db.query(CountHistory).all()
    log_query_result("CountHistory", len(count_history))
    return count_history
