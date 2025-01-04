from pydantic import BaseModel, Field
from datetime import datetime

class StateHistoryBase(BaseModel):
    start_datetime: datetime = Field(..., description="Start timestamp of the state")
    end_datetime: datetime = Field(..., description="End timestamp of the state")
    state_name: str = Field(..., max_length=100, description="Name of the state")
    reason_code: str = Field(..., max_length=20, description="Reason code for the state")

class StateHistoryCreate(StateHistoryBase):
    state_reason_id: int = Field(..., description="ID of the associated StateReason")
    line_id: int = Field(..., description="ID of the associated production line")
    run_id: int = Field(..., description="ID of the associated production run")

class StateHistoryOut(StateHistoryBase):
    id: int = Field(..., description="ID of the StateHistory")
    state_reason_id: int = Field(..., description="ID of the associated StateReason")
    line_id: int = Field(..., description="ID of the associated production line")
    run_id: int = Field(..., description="ID of the associated production run")

    class Config:
        orm_mode = True
