from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.downtime import StateReasonCreate, StateReasonUpdate, StateReasonOut, StateHistoryCreate, StateHistoryOut
from database.models.downtime import StateReason, StateHistory
from utils.dependencies import get_db
from auth.dependencies import get_current_user
from utils.exception_handler import CustomException

router = APIRouter(
    prefix="/downtime",
    tags=["Downtime"],
    dependencies=[Depends(get_current_user)]  # Protect all endpoints with JWT
)

# StateReason CRUD
@router.post("/state-reason/", response_model=StateReasonOut, status_code=status.HTTP_201_CREATED)
def create_state_reason(state_reason_in: StateReasonCreate, db: Session = Depends(get_db)):
    """
    Create a new StateReason.
    """
    existing = db.query(StateReason).filter(StateReason.reason_code == state_reason_in.reason_code).first()
    if existing:
        raise CustomException("StateReason with this code already exists.")
    new_state_reason = StateReason(**state_reason_in.dict())
    db.add(new_state_reason)
    db.commit()
    db.refresh(new_state_reason)
    return new_state_reason

@router.get("/state-reason/", response_model=List[StateReasonOut])
def get_all_state_reasons(db: Session = Depends(get_db)):
    """
    Retrieve all StateReasons.
    """
    return db.query(StateReason).all()

@router.put("/state-reason/{state_reason_id}", response_model=StateReasonOut)
def update_state_reason(state_reason_id: int, state_reason_upd: StateReasonUpdate, db: Session = Depends(get_db)):
    """
    Update an existing StateReason.
    """
    state_reason = db.query(StateReason).get(state_reason_id)
    if not state_reason:
        raise HTTPException(status_code=404, detail="StateReason not found.")
    for key, value in state_reason_upd.dict(exclude_unset=True).items():
        setattr(state_reason, key, value)
    db.commit()
    db.refresh(state_reason)
    return state_reason

@router.delete("/state-reason/{state_reason_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_state_reason(state_reason_id: int, db: Session = Depends(get_db)):
    """
    Delete a StateReason.
    """
    state_reason = db.query(StateReason).get(state_reason_id)
    if not state_reason:
        raise HTTPException(status_code=404, detail="StateReason not found.")
    db.delete(state_reason)
    db.commit()

# StateHistory CRUD
@router.post("/state-history/", response_model=StateHistoryOut, status_code=status.HTTP_201_CREATED)
def create_state_history(state_history_in: StateHistoryCreate, db: Session = Depends(get_db)):
    """
    Record a StateHistory entry.
    """
    # Ensure StateReason exists
    state_reason = db.query(StateReason).filter(StateReason.id == state_history_in.state_reason_id).first()
    if not state_reason:
        raise CustomException("Invalid StateReason.")
    new_state_history = StateHistory(**state_history_in.dict())
    db.add(new_state_history)
    db.commit()
    db.refresh(new_state_history)
    return new_state_history

@router.get("/state-history/", response_model=List[StateHistoryOut])
def get_all_state_histories(db: Session = Depends(get_db)):
    """
    Retrieve all StateHistories.
    """
    return db.query(StateHistory).all()
