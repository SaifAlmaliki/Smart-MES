# MES System

## Introduction

### What is MES?
A **Manufacturing Execution System (MES)** is software used to track and document the transformation of raw materials to finished goods in real time. This MES system provides:
- **OEE (Overall Equipment Effectiveness)** tracking.
- **Downtime management** to minimize unplanned production halts.
- **Work order management** for scheduling and tracking production tasks.
- **Production run and schedule management** to streamline workflows.

### Use Case
This MES system can:
- Track machine signals and calculate **OEE**.
- Record and analyze **downtime** events for better planning.
- Manage **work orders** to ensure production goals are met.
- Facilitate AI-powered recommendations for **predictive maintenance** and process optimization.
- Integrate with ERP systems for inventory and supply chain updates.

---

## Database Schema and Relationships

### **Database Models**
- Enterprise (1) ─── (M) Site
- Site (1) ─── (M) Area
- Area (1) ─── (M) Line
- Line (1) ─── (M) Schedule
- Schedule (1) ─── (M) Run
- CountType (1) ─── (M) CountTag
- CountTag (1) ─── (M) CountHistory
- StateReason (1) ─── (M) StateHistory


## Tables and Relationships
### Enterprise Structure (ISA-95 Hierarchy)
- Enterprise: Represents the organization.
- Site: Represents facilities within the organization.
- Area: Represents departments within a site.
- Line: Represents production lines within an area.
### OEE Tracking
- ProductionLine: Tracks availability, performance, and quality.
- OEE: Stores OEE calculations for production lines.
### Downtime Management
- StateReason: Lists reasons for downtime (planned/unplanned).
- StateHistory: Tracks historical downtime events.
### Work Order and Scheduling
- WorkOrder: Tracks production tasks.
- Schedule: Tracks planned production schedules.
- Run: Tracks real-time execution of production runs.

### Count Data
- CountType: Tracks different types of product counts (e.g., good, bad).
- CountTag: Tracks tags for sensors providing count data.
- CountHistory: Stores historical count data.

## API Endpoints
### Base URL: http://localhost:8000
- GET	/enterprise/	Retrieve all enterprises.
- POST	/enterprise/	Create a new enterprise.
- GET	/enterprise/{enterprise_id}	Retrieve a specific enterprise.

### Site, Area, Line
- GET	/site/	Retrieve all sites.
- POST	/site/	Create a new site.
- GET	/area/	Retrieve all areas.
- POST	/area/	Create a new area.
- GET	/line/	Retrieve all production lines.
- POST	/line/	Create a new production line.

### OEE Tracking
- GET	/oee/	Retrieve all OEE records.
- POST	/oee/	Create a new OEE record.
- GET	/oee/{oee_id}	Retrieve a specific OEE record.

### Downtime Management
- GET	/downtime/state-reason	Retrieve all downtime reasons.
- POST	/downtime/state-reason	Create a new downtime reason.
- GET	/downtime/state-history	Retrieve all downtime history records.
- POST	/downtime/state-history	Record a new downtime event.

### Work Order Management
- GET	/workorder/	Retrieve all work orders.
- POST	/workorder/	Create a new work order.
- PUT	/workorder/{work_order_id}	Update a specific work order.

### Schedule and Run Management
- GET	/schedule-run/schedule	Retrieve all schedules.
- POST	/schedule-run/schedule	Create a new schedule.
- GET	/schedule-run/run	Retrieve all runs.
- POST	/schedule-run/run	Create a new run.
- PUT	/schedule-run/run/{run_id}	Update a specific run.
