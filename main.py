from fastapi import FastAPI
from config import settings
from utils.exception_handler import add_custom_exception_handlers
from utils.logging_config import configure_logging
from routers import enterprise, site, area, line, cell, oee, downtime, workorder, schedule_run

def create_app() -> FastAPI:
    """
    Create and configure a FastAPI application.
    """
    # Configure logging
    configure_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API for MES System",
        version="1.0.0"
    )

    # Add custom exception handlers
    add_custom_exception_handlers(app)

    # Include routers
    app.include_router(enterprise.router)
    app.include_router(site.router)
    app.include_router(area.router)
    app.include_router(line.router)
    app.include_router(cell.router)
    app.include_router(oee.router)
    app.include_router(downtime.router)
    app.include_router(workorder.router)
    app.include_router(schedule_run.router)

    return app

app = create_app()
