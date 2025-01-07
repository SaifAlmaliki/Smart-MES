"""
Work order schemas for the MES system.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WorkOrderBase(BaseModel):
    """Base schema for work orders."""
    order_number: str = Field(..., max_length=50, description="Work order number/identifier")
    description: str = Field(..., max_length=500, description="Description of the work order")
    line_id: int = Field(..., description="ID of the production line")
    planned_start: datetime = Field(..., description="Planned start time")
    planned_end: datetime = Field(..., description="Planned end time")
    target_quantity: int = Field(..., gt=0, description="Target production quantity")
    status: str = Field(..., max_length=20, description="Current status of the work order")

class WorkOrderCreate(WorkOrderBase):
    """Schema for creating a work order."""
    pass

class WorkOrderUpdate(BaseModel):
    """Schema for updating a work order."""
    order_number: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    line_id: Optional[int] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    target_quantity: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None, max_length=20)

class WorkOrderOut(WorkOrderBase):
    """Schema for returning a work order."""
    id: int = Field(..., description="ID of the work order")
    actual_start: Optional[datetime] = Field(None, description="Actual start time")
    actual_end: Optional[datetime] = Field(None, description="Actual end time")
    actual_quantity: Optional[int] = Field(None, description="Actual production quantity")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        orm_mode = True
