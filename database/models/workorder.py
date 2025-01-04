"""
Work Order and Product Definitions:
- ProductCode
- ProductCodeLine
- WorkOrder
Splitting them out keeps product info distinct from the actual orders.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Base

class ProductCode(Base):
    __tablename__ = 'product_code'

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    disabled = Column(Boolean, default=False)

    # One-to-many
    product_code_lines = relationship("ProductCodeLine", back_populates="product_code_ref")
    work_orders = relationship("WorkOrder", back_populates="product_code")

class ProductCodeLine(Base):
    __tablename__ = 'product_code_line'

    id = Column(Integer, primary_key=True, index=True)
    product_code_id = Column(Integer, ForeignKey('product_code.id'), nullable=False)
    line_id = Column(Integer, ForeignKey('line.id'), nullable=False)

    product_code_ref = relationship("ProductCode", back_populates="product_code_lines")
    # line_ref is declared in enterprise.py. If you want a direct relationship here, do:
    # from enterprise import Line
    # line_ref = relationship("Line")

class WorkOrder(Base):
    __tablename__ = 'work_order'

    id = Column(Integer, primary_key=True, index=True)
    work_order_number = Column(String(50), nullable=False, unique=True)
    quantity = Column(Integer, default=0)
    closed = Column(Boolean, default=False)
    timestamp = Column(DateTime, nullable=False)

    # Link to product
    product_code_id = Column(Integer, ForeignKey('product_code.id'), nullable=True)
    product_code = relationship("ProductCode", back_populates="work_orders")
