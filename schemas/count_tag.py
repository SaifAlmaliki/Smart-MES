from pydantic import BaseModel, Field

class CountTagBase(BaseModel):
    tag_path: str = Field(..., max_length=255, description="Tag path for the count signal")

class CountTagCreate(CountTagBase):
    parent_id: int = Field(..., description="ID of the parent CountType")

class CountTagOut(CountTagBase):
    id: int = Field(..., description="ID of the CountTag")
    parent_id: int = Field(..., description="ID of the parent CountType")

    class Config:
        orm_mode = True
