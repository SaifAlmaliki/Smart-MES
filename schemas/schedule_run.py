from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schedule Schema
class ScheduleBase(BaseModel):
    line_id: int = Field(..., description="ID of the production line")
    schedule_type: str = Field(..., max_length=50, description="Type of schedule (e.g., planned, unplanned)")
    start_datetime: datetime = Field(..., description="Scheduled start time")
    finish_datetime: datetime = Field(..., description="Scheduled finish time")
    note: Optional[str] = Field(None, max_length=255, description="Optional notes for the schedule")

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    schedule_type: Optional[str] = Field(None, max_length=50)
    start_datetime: Optional[datetime] = Field(None)
    finish_datetime: Optional[datetime] = Field(None)
    note: Optional[str] = Field(None, max_length=255)

class ScheduleOut(ScheduleBase):
    id: int = Field(..., description="ID of the schedule")

    class Config:
        orm_mode = True


# Run Schema
class RunBase(BaseModel):
    schedule_id: int = Field(..., description="ID of the associated schedule")
    start_datetime: datetime = Field(..., description="Actual start time of the run")
    finish_datetime: Optional[datetime] = Field(None, description="Actual finish time of the run")
    status: str = Field(..., max_length=50, description="Status of the run (e.g., Running, Completed)")
    good_count: Optional[int] = Field(0, ge=0, description="Count of good products produced")
    bad_count: Optional[int] = Field(0, ge=0, description="Count of bad products produced")

class RunCreate(RunBase):
    pass

class RunUpdate(BaseModel):
    finish_datetime: Optional[datetime] = Field(None)
    status: Optional[str] = Field(None, max_length=50)
    good_count: Optional[int] = Field(None, ge=0)
    bad_count: Optional[int] = Field(None, ge=0)

class RunOut(RunBase):
    id: int = Field(..., description="ID of the run")

    class Config:
        orm_mode = True
