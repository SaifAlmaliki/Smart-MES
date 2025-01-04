"""
Downtime tracking tables:
- StateReason: hierarchical downtime reasons
- StateHistory: logs downtime or state changes
Splitting these helps track reasons and logs separately.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Base

class StateReason(Base):
    __tablename__ = 'state_reason'

    id = Column(Integer, primary_key=True, index=True)
    reason_name = Column(String(255), nullable=False)
    reason_code = Column(String(50), nullable=False, unique=True)
    record_downtime = Column(Boolean, default=False)
    planned_downtime = Column(Boolean, default=False)
    operator_selectable = Column(Boolean, default=True)

    # Hierarchical parent-child downtime reasons
    parent_id = Column(Integer, ForeignKey('state_reason.id'), nullable=True)
    sub_reasons = relationship("StateReason", backref="parent", remote_side=[id])

class StateHistory(Base):
    __tablename__ = 'state_history'

    id = Column(Integer, primary_key=True, index=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=True)

    # Reason fields
    state_reason_id = Column(Integer, ForeignKey('state_reason.id'), nullable=False)
    reason_name = Column(String(255), nullable=False)
    reason_code = Column(String(50), nullable=False)

    # Reference to a line or run
    line_id = Column(Integer, ForeignKey('line.id'), nullable=True)
    run_id = Column(Integer, ForeignKey('run.id'), nullable=True)

    # Relationship
    state_reason = relationship("StateReason")
    # line relationship is in enterprise.py: you can import it, or do a lazy relationship
    # run relationship will be in schedule_run.py
