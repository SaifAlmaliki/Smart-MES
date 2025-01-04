from pydantic import BaseModel, Field
from typing import Optional

class WorkOrderBase(BaseModel):
    product_code: str = Field(..., max_length=50, description="Product code for the work order")
    quantity: int = Field(..., gt=0, description="Quantity of items in the work order")
    status: str = Field(..., max_length=20, description="Status of the work order (e.g., Open, Completed)")

class WorkOrderCreate(WorkOrderBase):
    pass

class WorkOrderUpdate(BaseModel):
    product_code: Optional[str] = Field(None, max_length=50)
    quantity: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None, max_length=20)

class WorkOrderOut(WorkOrderBase):
    id: int = Field(..., description="ID of the work order")

    class Config:
        orm_mode = True
