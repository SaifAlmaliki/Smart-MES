"""
Scheduling and production runs:
We split Run into:
- Run (basic info about the run)
- RunMetrics (detailed run metrics such as availability, performance, etc.)
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.engine import Base

class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, index=True)
    schedule_type = Column(String(50), nullable=True)
    note = Column(String(255), nullable=True)
    schedule_start_datetime = Column(DateTime, nullable=True)
    schedule_finish_datetime = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, nullable=False)

    # Foreign keys
    line_id = Column(Integer, ForeignKey('line.id'), nullable=False)
    work_order_id = Column(Integer, ForeignKey('work_order.id'), nullable=True)

    # Relationship
    line = relationship("Line", backref="schedules")
    work_order = relationship("WorkOrder", backref="schedules")
    runs = relationship("Run", back_populates="schedule")

class Run(Base):
    __tablename__ = 'run'

    id = Column(Integer, primary_key=True, index=True)

    schedule_id = Column(Integer, ForeignKey('schedule.id'), nullable=False)
    run_start_datetime = Column(DateTime, nullable=True)
    run_stop_datetime = Column(DateTime, nullable=True)
    closed = Column(Boolean, default=False)
    estimated_finish_time = Column(DateTime, nullable=True)

    # Relationship to schedule
    schedule = relationship("Schedule", back_populates="runs")

    # Relationship to downtime logs
    # This matches the downtime model
    state_histories = relationship("StateHistory", backref="run")

    # One-to-one or one-to-many for run metrics
    run_metrics = relationship("RunMetrics", back_populates="run", uselist=False)

class RunMetrics(Base):
    __tablename__ = 'run_metrics'

    id = Column(Integer, primary_key=True, index=True)

    # Link to Run (one-to-one)
    run_id = Column(Integer, ForeignKey('run.id'), nullable=False, unique=True)

    good_count = Column(Integer, default=0)
    waste_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)

    availability = Column(Float, default=0.0)
    performance = Column(Float, default=0.0)
    quality = Column(Float, default=0.0)
    oee = Column(Float, default=0.0)

    unplanned_downtime = Column(Float, default=0.0)
    planned_downtime = Column(Float, default=0.0)
    total_time = Column(Float, default=0.0)

    run = relationship("Run", back_populates="run_metrics")
