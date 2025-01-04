from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.schedule_run import ScheduleCreate, ScheduleUpdate, ScheduleOut, RunCreate, RunUpdate, RunOut
from database import get_db
from models.schedule_run import Schedule, Run

router = APIRouter(
    prefix="/schedule-run",
    tags=["Schedule and Run"]
)

# Schedule Routes
@router.post("/schedule", response_model=ScheduleOut, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule_in: ScheduleCreate, db: Session = Depends(get_db)):
    """
    Create a new schedule.
    """
    new_schedule = Schedule(**schedule_in.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

@router.get("/schedule", response_model=List[ScheduleOut])
def get_all_schedules(db: Session = Depends(get_db)):
    """
    Retrieve all schedules.
    """
    return db.query(Schedule).all()

# Run Routes
@router.post("/run", response_model=RunOut, status_code=status.HTTP_201_CREATED)
def create_run(run_in: RunCreate, db: Session = Depends(get_db)):
    """
    Create a new production run.
    """
    new_run = Run(**run_in.dict())
    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    return new_run

@router.get("/run", response_model=List[RunOut])
def get_all_runs(db: Session = Depends(get_db)):
    """
    Retrieve all production runs.
    """
    return db.query(Run).all()

@router.put("/run/{run_id}", response_model=RunOut)
def update_run(run_id: int, run_upd: RunUpdate, db: Session = Depends(get_db)):
    """
    Update an existing production run.
    """
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")
    for key, value in run_upd.dict(exclude_unset=True).items():
        setattr(run, key, value)
    db.commit()
    db.refresh(run)
    return run
