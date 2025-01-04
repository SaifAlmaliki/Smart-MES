# file: seed.py

from datetime import datetime
from sqlalchemy.orm import Session
from database.engine import engine, SessionLocal, Base
from database.models.enterprise import Enterprise, Site, Area, Line, Cell
from database.models.oee import CountType, CountTag
from database.models.workorder import WorkOrder, ProductCode
from database.models.schedule_run import Schedule, Run, RunMetrics
from database.models.downtime import StateReason, StateHistory

# Pydantic Schemas
from schemas.enterprise import EnterpriseCreate, SiteCreate

def seed_database():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1) Enterprise
        enterprise_data = EnterpriseCreate(
            name="Global Manufacturing Co.",
            timestamp=datetime.utcnow()
        )
        new_enterprise = Enterprise(**enterprise_data.dict())
        db.add(new_enterprise)
        db.commit()
        db.refresh(new_enterprise)

        # 2) Site
        site_data = SiteCreate(
            name="Main Plant",
            timestamp=datetime.utcnow(),
            enterprise_id=new_enterprise.id
        )
        new_site = Site(**site_data.dict())
        db.add(new_site)
        db.commit()
        db.refresh(new_site)

        # 3) Add an Area, Line, Cell
        packaging_area = Area(name="Packaging Area", timestamp=datetime.utcnow(), site_id=new_site.id)
        db.add(packaging_area)
        db.commit()
        db.refresh(packaging_area)

        line1 = Line(name="Line #1", timestamp=datetime.utcnow(), area_id=packaging_area.id)
        db.add(line1)
        db.commit()
        db.refresh(line1)

        cell1 = Cell(name="Labeler Cell", timestamp=datetime.utcnow(), line_id=line1.id)
        db.add(cell1)
        db.commit()
        db.refresh(cell1)

        # 4) Seed OEE Data
        count_type_good = CountType(count_type="Good")
        count_type_scrap = CountType(count_type="Scrap")
        db.add_all([count_type_good, count_type_scrap])
        db.commit()

        tag_good = CountTag(tag_path="Line1/GoodCount")
        tag_scrap = CountTag(tag_path="Line1/ScrapCount")
        db.add_all([tag_good, tag_scrap])
        db.commit()

        # 5) Product and Work Order
        product_code = ProductCode(product_code="SKU-1234", description="Example Product", disabled=False)
        db.add(product_code)
        db.commit()
        db.refresh(product_code)

        work_order1 = WorkOrder(work_order_number="WO-1001", quantity=1000, timestamp=datetime.utcnow(), product_code_id=product_code.id)
        db.add(work_order1)
        db.commit()
        db.refresh(work_order1)

        # 6) Schedule and Run
        schedule1 = Schedule(schedule_type="Production", note="Initial run", schedule_start_datetime=datetime.utcnow(),
                             timestamp=datetime.utcnow(), line_id=line1.id, work_order_id=work_order1.id)
        db.add(schedule1)
        db.commit()
        db.refresh(schedule1)

        run1 = Run(schedule_id=schedule1.id, run_start_datetime=datetime.utcnow(), closed=False)
        db.add(run1)
        db.commit()
        db.refresh(run1)

        # 6.1) Create Run Metrics for run1
        metrics1 = RunMetrics(
            run_id=run1.id,
            good_count=0, waste_count=0, total_count=0,
            availability=0.0, performance=0.0, quality=0.0, oee=0.0,
            unplanned_downtime=0.0, planned_downtime=0.0, total_time=0.0
        )
        db.add(metrics1)
        db.commit()

        # 7) Downtime States
        sr_planned = StateReason(reason_name="Planned Maintenance", reason_code="PM01", record_downtime=True, planned_downtime=True)
        sr_unplanned = StateReason(reason_name="Unplanned Breakdown", reason_code="UB01", record_downtime=True, planned_downtime=False)
        db.add_all([sr_planned, sr_unplanned])
        db.commit()
        db.refresh(sr_planned)
        db.refresh(sr_unplanned)

        # 7.1) Sample downtime
        downtime_rec = StateHistory(
            start_datetime=datetime.utcnow(),
            end_datetime=datetime.utcnow(),
            state_reason_id=sr_unplanned.id,
            reason_name=sr_unplanned.reason_name,
            reason_code=sr_unplanned.reason_code,
            line_id=line1.id,
            run_id=run1.id
        )
        db.add(downtime_rec)
        db.commit()

        print("Seeded database successfully!")

    except Exception as exc:
        db.rollback()
        print(f"Error seeding database: {exc}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
