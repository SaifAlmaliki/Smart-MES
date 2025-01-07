from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schedule Schema
class ScheduleBase(BaseModel):
    line_id: int = Field(..., description="ID of the production line")
    schedule_type: str = Field(..., max_length=50, description="Type of schedule (e.g., planned, unplanned)")
    schedule_start_datetime: datetime = Field(..., description="Scheduled start time")
    schedule_finish_datetime: datetime = Field(..., description="Scheduled finish time")
    note: Optional[str] = Field(None, max_length=255, description="Optional notes for the schedule")

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    schedule_type: Optional[str] = Field(None, max_length=50)
    schedule_start_datetime: Optional[datetime] = Field(None)
    schedule_finish_datetime: Optional[datetime] = Field(None)
    note: Optional[str] = Field(None, max_length=255)

class ScheduleOut(ScheduleBase):
    id: int = Field(..., description="ID of the schedule")

    class Config:
        orm_mode = True


# Run Schema
class RunBase(BaseModel):
    schedule_id: int = Field(..., description="ID of the associated schedule")
    run_start_datetime: datetime = Field(..., description="Actual start time of the run")
    run_stop_datetime: Optional[datetime] = Field(None, description="Actual finish time of the run")
    closed: bool = Field(default=False, description="Whether the run is closed")
    estimated_finish_time: Optional[datetime] = Field(None, description="Estimated finish time of the run")

class RunCreate(RunBase):
    pass

class RunUpdate(BaseModel):
    run_stop_datetime: Optional[datetime] = Field(None)
    closed: Optional[bool] = Field(None)
    estimated_finish_time: Optional[datetime] = Field(None)

class RunOut(RunBase):
    id: int = Field(..., description="ID of the run")

    class Config:
        orm_mode = True
