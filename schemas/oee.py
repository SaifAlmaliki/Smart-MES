from pydantic import BaseModel, Field

class OEEBase(BaseModel):
    availability: float = Field(..., ge=0, le=1, description="Availability metric")
    performance: float = Field(..., ge=0, le=1, description="Performance metric")
    quality: float = Field(..., ge=0, le=1, description="Quality metric")

class OEECreate(OEEBase):
    line_id: int = Field(..., description="ID of the production line associated with this OEE")

class OEEOut(OEEBase):
    id: int = Field(..., description="ID of the OEE record")
    line_id: int = Field(..., description="ID of the production line associated with this OEE")
    oee: float = Field(..., description="Calculated OEE value")

    class Config:
        orm_mode = True
