from pydantic import BaseModel, Field

class StateReasonBase(BaseModel):
    reason_name: str = Field(..., max_length=100, description="Name of the state reason")
    reason_code: str = Field(..., max_length=20, description="Code for the state reason")
    record_downtime: bool = Field(..., description="Whether to record downtime for this reason")
    planned_downtime: bool = Field(..., description="Whether this is planned downtime")

class StateReasonCreate(StateReasonBase):
    parent_id: int = Field(..., description="ID of the parent reason")

class StateReasonUpdate(BaseModel):
    reason_name: Optional[str] = Field(None, max_length=100)
    reason_code: Optional[str] = Field(None, max_length=20)
    record_downtime: Optional[bool] = Field(None)
    planned_downtime: Optional[bool] = Field(None)

class StateReasonOut(StateReasonBase):
    id: int = Field(..., description="ID of the StateReason")
    parent_id: int = Field(..., description="ID of the parent reason")

    class Config:
        orm_mode = True
