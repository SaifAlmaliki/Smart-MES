from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.schedule_run import (
    ScheduleCreate, ScheduleUpdate, ScheduleOut,
    RunCreate, RunUpdate, RunOut
)
from database.models.schedule_run import Schedule, Run
from database.models.enterprise import Line
from utils.dependencies import get_db

router = APIRouter(
    prefix="/schedule-run",
    tags=["ScheduleRun"]
)

# Schedule Routes
@router.post("/schedule", response_model=ScheduleOut, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule_in: ScheduleCreate, db: Session = Depends(get_db)):
    """
    Create a new schedule.
    """
    # Validate line exists
    line = db.query(Line).filter(Line.id == schedule_in.line_id).first()
    if not line:
        raise HTTPException(status_code=404, detail="Production line not found")

    new_schedule = Schedule(
        line_id=schedule_in.line_id,
        schedule_type=schedule_in.schedule_type,
        schedule_start_datetime=schedule_in.start_datetime,
        schedule_finish_datetime=schedule_in.finish_datetime,
        note=schedule_in.note,
        timestamp=schedule_in.start_datetime
    )
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
    # Validate schedule exists
    schedule = db.query(Schedule).filter(Schedule.id == run_in.schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    new_run = Run(
        schedule_id=run_in.schedule_id,
        run_start_datetime=run_in.start_datetime,
        run_stop_datetime=run_in.finish_datetime,
        closed=(run_in.status.lower() == "completed"),
        estimated_finish_time=schedule.schedule_finish_datetime
    )
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
def update_run(run_id: int, run_in: RunUpdate, db: Session = Depends(get_db)):
    """
    Update an existing production run.
    """
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run_in.finish_datetime:
        run.run_stop_datetime = run_in.finish_datetime
    if run_in.status:
        run.closed = (run_in.status.lower() == "completed")

    db.commit()
    db.refresh(run)
    return run
