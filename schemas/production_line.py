from pydantic import BaseModel, Field
from typing import Optional

class ProductionLineBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the production line")
    availability: Optional[float] = Field(None, ge=0, le=1, description="Availability metric")
    performance: Optional[float] = Field(None, ge=0, le=1, description="Performance metric")
    quality: Optional[float] = Field(None, ge=0, le=1, description="Quality metric")

class ProductionLineCreate(ProductionLineBase):
    pass

class ProductionLineUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    availability: Optional[float] = Field(None, ge=0, le=1)
    performance: Optional[float] = Field(None, ge=0, le=1)
    quality: Optional[float] = Field(None, ge=0, le=1)

class ProductionLineOut(ProductionLineBase):
    id: int = Field(..., description="ID of the production line")

    class Config:
        orm_mode = True
