"""
OEE-related tables (CountType, CountTag, CountHistory).
Splitting out 'CountHistory' into its own table helps manage large volumes (high-frequency data).
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Base

class CountType(Base):
    __tablename__ = 'count_type'

    id = Column(Integer, primary_key=True, index=True)
    count_type = Column(String(100), nullable=False, unique=True)

    # One-to-many: CountType -> CountHistory
    count_histories = relationship("CountHistory", back_populates="count_type_ref")

class CountTag(Base):
    __tablename__ = 'count_tag'

    id = Column(Integer, primary_key=True, index=True)
    tag_path = Column(String(255), nullable=False, unique=True)

    parent_id = Column(Integer, nullable=True)  # optional if you have a parent-child tag structure

    # One-to-many: CountTag -> CountHistory
    count_histories = relationship("CountHistory", back_populates="count_tag")

class CountHistory(Base):
    __tablename__ = 'count_history'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    count = Column(Integer, nullable=False)

    tag_id = Column(Integer, ForeignKey('count_tag.id'), nullable=False)
    count_type_id = Column(Integer, ForeignKey('count_type.id'), nullable=False)

    # Optional link to production run
    run_id = Column(Integer, ForeignKey('run.id'), nullable=True)

    # Relationships
    count_tag = relationship("CountTag", back_populates="count_histories")
    count_type_ref = relationship("CountType", back_populates="count_histories")
