"""
Seed script for MES database.
Creates realistic sample data for all tables in the correct order to maintain relationships.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.engine import SessionLocal, engine
from database.models.enterprise import Enterprise, Site, Area, Line, Cell
from database.models.workorder import WorkOrder, ProductCode, ProductCodeLine
from database.models.schedule_run import Schedule, Run
from database.models.oee import CountType, CountTag, CountHistory
from database.models.downtime import StateHistory, StateReason

def seed_data():
    db = SessionLocal()
    try:
        # Clear existing data (optional)
        clear_existing_data(db)
        
        # 1. Create Enterprise
        enterprise = Enterprise(
            name="TechManufacturing Inc.",
            timestamp=datetime.utcnow(),
            disabled=False
        )
        db.add(enterprise)
        db.flush()  # Get ID before continuing

        # 2. Create Sites
        sites = [
            Site(
                name="North America Production Hub",
                enterprise_id=enterprise.id,
                timestamp=datetime.utcnow(),
                disabled=False
            ),
            Site(
                name="European Manufacturing Center",
                enterprise_id=enterprise.id,
                timestamp=datetime.utcnow(),
                disabled=False
            )
        ]
        db.add_all(sites)
        db.flush()

        # 3. Create Areas
        areas = [
            Area(
                name="Assembly Division",
                site_id=sites[0].id,
                timestamp=datetime.utcnow(),
                disabled=False
            ),
            Area(
                name="Packaging Department",
                site_id=sites[0].id,
                timestamp=datetime.utcnow(),
                disabled=False
            ),
            Area(
                name="Quality Control",
                site_id=sites[1].id,
                timestamp=datetime.utcnow(),
                disabled=False
            )
        ]
        db.add_all(areas)
        db.flush()

        # 4. Create Production Lines
        lines = [
            Line(
                name="Main Assembly Line",
                area_id=areas[0].id,
                timestamp=datetime.utcnow(),
                disabled=False
            ),
            Line(
                name="Secondary Assembly Line",
                area_id=areas[0].id,
                timestamp=datetime.utcnow(),
                disabled=False
            ),
            Line(
                name="Packaging Line 1",
                area_id=areas[1].id,
                timestamp=datetime.utcnow(),
                disabled=False
            )
        ]
        db.add_all(lines)
        db.flush()

        # 5. Create Cells
        cells = [
            Cell(
                name="Station 1 - Component Assembly",
                line_id=lines[0].id,
                timestamp=datetime.utcnow(),
                disabled=False
            ),
            Cell(
                name="Station 2 - Testing",
                line_id=lines[0].id,
                timestamp=datetime.utcnow(),
                disabled=False
            ),
            Cell(
                name="Station 3 - Final Assembly",
                line_id=lines[0].id,
                timestamp=datetime.utcnow(),
                disabled=False
            )
        ]
        db.add_all(cells)
        db.flush()

        # 6. Create Product Codes
        product_codes = [
            ProductCode(
                product_code="WIDGET-001",
                description="Standard Widget Assembly",
                disabled=False
            ),
            ProductCode(
                product_code="WIDGET-002",
                description="Premium Widget Assembly",
                disabled=False
            )
        ]
        db.add_all(product_codes)
        db.flush()

        # 7. Create Product Code Lines (linking products to lines)
        product_code_lines = [
            ProductCodeLine(
                product_code_id=product_codes[0].id,
                line_id=lines[0].id
            ),
            ProductCodeLine(
                product_code_id=product_codes[1].id,
                line_id=lines[0].id
            )
        ]
        db.add_all(product_code_lines)
        db.flush()

        # 8. Create Work Orders
        current_time = datetime.utcnow()
        work_orders = [
            WorkOrder(
                order_number="WO-2025-001",
                description="Standard Widget Production Batch",
                line_id=lines[0].id,
                planned_start=current_time + timedelta(hours=1),
                planned_end=current_time + timedelta(hours=9),
                target_quantity=1000,
                status="Planned",
                product_code_id=product_codes[0].id
            ),
            WorkOrder(
                order_number="WO-2025-002",
                description="Premium Widget Production Batch",
                line_id=lines[0].id,
                planned_start=current_time + timedelta(days=1),
                planned_end=current_time + timedelta(days=1, hours=8),
                target_quantity=500,
                status="Planned",
                product_code_id=product_codes[1].id
            )
        ]
        db.add_all(work_orders)
        db.flush()

        # 9. Create Schedules
        schedules = [
            Schedule(
                line_id=lines[0].id,
                schedule_type="Production",
                schedule_start_datetime=current_time + timedelta(hours=1),
                schedule_finish_datetime=current_time + timedelta(hours=9),
                note="Morning Shift Production",
                timestamp=current_time,
                work_order_id=work_orders[0].id
            ),
            Schedule(
                line_id=lines[0].id,
                schedule_type="Production",
                schedule_start_datetime=current_time + timedelta(days=1),
                schedule_finish_datetime=current_time + timedelta(days=1, hours=8),
                note="Next Day Production",
                timestamp=current_time,
                work_order_id=work_orders[1].id
            )
        ]
        db.add_all(schedules)
        db.flush()

        # 10. Create Runs
        runs = [
            Run(
                schedule_id=schedules[0].id,
                run_start_datetime=current_time + timedelta(hours=1),
                estimated_finish_time=current_time + timedelta(hours=9),
                closed=False
            )
        ]
        db.add_all(runs)
        db.flush()

        # 11. Create Count Types
        count_types = [
            CountType(
                name="Good Count",
                description="Products that passed all quality checks"
            ),
            CountType(
                name="Defect Count",
                description="Products that failed quality checks"
            ),
            CountType(
                name="Rework Count",
                description="Products that need rework"
            )
        ]
        db.add_all(count_types)
        db.flush()

        # 12. Create Count Tags
        count_tags = [
            CountTag(
                name="Pass",
                description="Passed all quality checks",
                count_type_id=count_types[0].id
            ),
            CountTag(
                name="Minor Defect",
                description="Failed due to minor issues",
                count_type_id=count_types[1].id
            ),
            CountTag(
                name="Major Defect",
                description="Failed due to major issues",
                count_type_id=count_types[1].id
            ),
            CountTag(
                name="Assembly Rework",
                description="Needs reassembly",
                count_type_id=count_types[2].id
            )
        ]
        db.add_all(count_tags)
        db.flush()

        # 13. Create Count History (last hour of production)
        count_histories = []
        for i in range(6):  # Last hour in 10-minute intervals
            time_point = current_time + timedelta(hours=1, minutes=i*10)
            
            # Good counts (varying between 80-100 pieces)
            count_histories.append(
                CountHistory(
                    count=80 + (i * 5),
                    timestamp=time_point,
                    tag_id=count_tags[0].id,
                    count_type_id=count_types[0].id,
                    run_id=runs[0].id
                )
            )
            
            # Defect counts (about 5% defect rate)
            if i % 2 == 0:  # Every 20 minutes
                count_histories.append(
                    CountHistory(
                        count=4 + (i % 3),
                        timestamp=time_point,
                        tag_id=count_tags[1].id,
                        count_type_id=count_types[1].id,
                        run_id=runs[0].id
                    )
                )
            
            # Rework counts (about 2% rework rate)
            if i % 3 == 0:  # Every 30 minutes
                count_histories.append(
                    CountHistory(
                        count=2,
                        timestamp=time_point,
                        tag_id=count_tags[3].id,
                        count_type_id=count_types[2].id,
                        run_id=runs[0].id
                    )
                )

        db.add_all(count_histories)
        db.flush()

        # 14. Create State Reasons
        state_reasons = [
            StateReason(
                reason_name="Planned Maintenance",
                reason_code="PM-001",
                record_downtime=True,
                planned_downtime=True,
                operator_selectable=True
            ),
            StateReason(
                reason_name="Equipment Failure",
                reason_code="EF-001",
                record_downtime=True,
                planned_downtime=False,
                operator_selectable=True
            ),
            StateReason(
                reason_name="Material Shortage",
                reason_code="MS-001",
                record_downtime=True,
                planned_downtime=False,
                operator_selectable=True
            )
        ]
        db.add_all(state_reasons)
        db.flush()

        # Add sub-reasons
        sub_reasons = [
            StateReason(
                reason_name="Preventive Maintenance",
                reason_code="PM-001-01",
                record_downtime=True,
                planned_downtime=True,
                operator_selectable=True,
                parent_id=state_reasons[0].id
            ),
            StateReason(
                reason_name="Mechanical Failure",
                reason_code="EF-001-01",
                record_downtime=True,
                planned_downtime=False,
                operator_selectable=True,
                parent_id=state_reasons[1].id
            ),
            StateReason(
                reason_name="Electrical Failure",
                reason_code="EF-001-02",
                record_downtime=True,
                planned_downtime=False,
                operator_selectable=True,
                parent_id=state_reasons[1].id
            )
        ]
        db.add_all(sub_reasons)
        db.flush()

        # 15. Create State History (some downtime events during the run)
        state_histories = [
            StateHistory(
                start_datetime=current_time + timedelta(hours=2),
                end_datetime=current_time + timedelta(hours=2, minutes=15),
                state_reason_id=sub_reasons[1].id,  # Mechanical Failure
                reason_name=sub_reasons[1].reason_name,
                reason_code=sub_reasons[1].reason_code,
                line_id=lines[0].id,
                run_id=runs[0].id
            ),
            StateHistory(
                start_datetime=current_time + timedelta(hours=4),
                end_datetime=current_time + timedelta(hours=4, minutes=30),
                state_reason_id=sub_reasons[0].id,  # Preventive Maintenance
                reason_name=sub_reasons[0].reason_name,
                reason_code=sub_reasons[0].reason_code,
                line_id=lines[0].id,
                run_id=runs[0].id
            )
        ]
        db.add_all(state_histories)
        
        # Commit all changes
        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def clear_existing_data(db: Session):
    """Clear all existing data from tables in reverse order of dependencies."""
    db.query(CountHistory).delete()
    db.query(CountTag).delete()
    db.query(CountType).delete()
    db.query(StateHistory).delete()
    db.query(StateReason).delete()
    db.query(Run).delete()
    db.query(Schedule).delete()
    db.query(WorkOrder).delete()
    db.query(ProductCodeLine).delete()
    db.query(ProductCode).delete()
    db.query(Cell).delete()
    db.query(Line).delete()
    db.query(Area).delete()
    db.query(Site).delete()
    db.query(Enterprise).delete()
    db.commit()

if __name__ == "__main__":
    seed_data()
