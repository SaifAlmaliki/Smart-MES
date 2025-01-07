"""
Defines the enterprise hierarchy (ISA-95 Levels):
- Enterprise
- Site
- Area
- Line
- Cell
Splitting these into separate tables ensures each level can scale independently.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Base

class Enterprise(Base):
    __tablename__ = 'enterprise'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    timestamp = Column(DateTime, nullable=False)
    disabled = Column(Boolean, default=False)

    # One-to-many: Enterprise -> Site
    sites = relationship("Site", back_populates="enterprise")

class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    timestamp = Column(DateTime, nullable=False)
    disabled = Column(Boolean, default=False)

    enterprise_id = Column(Integer, ForeignKey('enterprise.id'))
    enterprise = relationship("Enterprise", back_populates="sites")

    # One-to-many: Site -> Area
    areas = relationship("Area", back_populates="site")

class Area(Base):
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    disabled = Column(Boolean, default=False)

    site_id = Column(Integer, ForeignKey('site.id'))
    site = relationship("Site", back_populates="areas")

    # One-to-many: Area -> Line
    lines = relationship("Line", back_populates="area")

class Line(Base):
    __tablename__ = 'line'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    disabled = Column(Boolean, default=False)

    area_id = Column(Integer, ForeignKey('area.id'))
    area = relationship("Area", back_populates="lines")

    # One-to-many: Line -> Cell
    cells = relationship("Cell", back_populates="line")
    # One-to-many: Line -> WorkOrder
    work_orders = relationship("WorkOrder", back_populates="line")
    # One-to-many: Line -> OEE
    oee_records = relationship("OEE", back_populates="line")

class Cell(Base):
    __tablename__ = 'cell'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    disabled = Column(Boolean, default=False)

    line_id = Column(Integer, ForeignKey('line.id'))
    line = relationship("Line", back_populates="cells")
