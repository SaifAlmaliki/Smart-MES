from pydantic import BaseModel, Field

class CountTypeBase(BaseModel):
    count_type: str = Field(..., max_length=50, description="Type of count (e.g., Good, Bad)")

class CountTypeCreate(CountTypeBase):
    pass

class CountTypeUpdate(BaseModel):
    count_type: Optional[str] = Field(None, max_length=50)

class CountTypeOut(CountTypeBase):
    id: int = Field(..., description="ID of the CountType")

    class Config:
        orm_mode = True
