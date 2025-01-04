from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# StateReason Schema
class StateReasonBase(BaseModel):
    reason_name: str = Field(..., max_length=100, description="Name of the downtime reason")
    reason_code: str = Field(..., max_length=50, description="Unique code for the reason")
    record_downtime: bool = Field(..., description="Indicates if downtime should be recorded")
    planned_downtime: bool = Field(..., description="Indicates if this is planned downtime")
    operator_selectable: bool = Field(..., description="Indicates if the operator can select this reason")
    sub_reason_of: Optional[int] = Field(None, description="ID of the parent reason, if applicable")

class StateReasonCreate(StateReasonBase):
    pass

class StateReasonUpdate(BaseModel):
    reason_name: Optional[str] = Field(None, max_length=100)
    reason_code: Optional[str] = Field(None, max_length=50)
    record_downtime: Optional[bool] = Field(None)
    planned_downtime: Optional[bool] = Field(None)
    operator_selectable: Optional[bool] = Field(None)
    sub_reason_of: Optional[int] = Field(None)

class StateReasonOut(StateReasonBase):
    id: int = Field(..., description="ID of the StateReason")

    class Config:
        orm_mode = True


# StateHistory Schema
class StateHistoryBase(BaseModel):
    start_datetime: datetime = Field(..., description="Start time of the state")
    end_datetime: datetime = Field(..., description="End time of the state")
    state_name: str = Field(..., max_length=100, description="Name of the state")
    reason_code: str = Field(..., max_length=50, description="Reason code for the state")

class StateHistoryCreate(StateHistoryBase):
    state_reason_id: int = Field(..., description="ID of the associated StateReason")
    line_id: int = Field(..., description="ID of the production line")
    run_id: int = Field(..., description="ID of the associated production run")

class StateHistoryOut(StateHistoryBase):
    id: int = Field(..., description="ID of the StateHistory")
    state_reason_id: int = Field(..., description="ID of the associated StateReason")
    line_id: int = Field(..., description="ID of the production line")
    run_id: int = Field(..., description="ID of the associated production run")

    class Config:
        orm_mode = True
