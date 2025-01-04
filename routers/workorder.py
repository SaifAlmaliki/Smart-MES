from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.work_order import WorkOrderCreate, WorkOrderUpdate, WorkOrderOut
from database import get_db
from models.workorder import WorkOrder

router = APIRouter(
    prefix="/workorder",
    tags=["WorkOrder"]
)

@router.post("/", response_model=WorkOrderOut, status_code=status.HTTP_201_CREATED)
def create_work_order(order_in: WorkOrderCreate, db: Session = Depends(get_db)):
    """
    Create a new work order.
    """
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
def update_work_order(work_order_id: int, order_upd: WorkOrderUpdate, db: Session = Depends(get_db)):
    """
    Update an existing work order.
    """
    order = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Work order not found.")
    for key, value in order_upd.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order
