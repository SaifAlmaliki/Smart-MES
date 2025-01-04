from pydantic import BaseModel, Field
from datetime import datetime

class CountHistoryBase(BaseModel):
    count: int = Field(..., gt=0, description="Count value")
    timestamp: datetime = Field(..., description="Timestamp of the count event")

class CountHistoryCreate(CountHistoryBase):
    tag_id: int = Field(..., description="ID of the associated CountTag")
    count_type_id: int = Field(..., description="ID of the associated CountType")
    run_id: int = Field(..., description="ID of the associated production run")

class CountHistoryOut(CountHistoryBase):
    id: int = Field(..., description="ID of the CountHistory")
    tag_id: int = Field(..., description="ID of the associated CountTag")
    count_type_id: int = Field(..., description="ID of the associated CountType")
    run_id: int = Field(..., description="ID of the associated production run")

    class Config:
        orm_mode = True
