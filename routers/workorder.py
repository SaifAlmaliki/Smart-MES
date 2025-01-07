from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.work_order import WorkOrderCreate, WorkOrderUpdate, WorkOrderOut
from database.models.workorder import WorkOrder
from database.models.enterprise import Line
from utils.dependencies import get_db

router = APIRouter(
    prefix="/workorder",
    tags=["WorkOrder"]
)

@router.post("/", response_model=WorkOrderOut, status_code=status.HTTP_201_CREATED)
def create_work_order(order_in: WorkOrderCreate, db: Session = Depends(get_db)):
    """
    Create a new work order.
    """
    # Validate line exists
    line = db.query(Line).filter(Line.id == order_in.line_id).first()
    if not line:
        raise HTTPException(status_code=404, detail="Production line not found")

    new_order = WorkOrder(**order_in.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=List[WorkOrderOut])
def get_all_work_orders(db: Session = Depends(get_db)):
    """
    Retrieve all work orders.
    """
    return db.query(WorkOrder).all()

@router.put("/{work_order_id}", response_model=WorkOrderOut)
def update_work_order(work_order_id: int, order_in: WorkOrderUpdate, db: Session = Depends(get_db)):
    """
    Update a work order.
    """
    work_order = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")

    # If line_id is being updated, validate new line exists
    if order_in.line_id is not None:
        line = db.query(Line).filter(Line.id == order_in.line_id).first()
        if not line:
            raise HTTPException(status_code=404, detail="Production line not found")

    for field, value in order_in.dict(exclude_unset=True).items():
        setattr(work_order, field, value)

    db.commit()
    db.refresh(work_order)
    return work_order
