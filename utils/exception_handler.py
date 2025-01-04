from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

class CustomException(Exception):
    """
    Custom application exception for handling business logic errors.
    """
    def __init__(self, detail: str, status_code: int = HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code

def add_custom_exception_handlers(app):
    """
    Add global exception handlers to the FastAPI app.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Handle HTTP exceptions (e.g., 404, 401).
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        """
        Handle custom exceptions.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """
        Handle validation errors raised by Pydantic or FastAPI.
        """
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """
        Handle database integrity errors (e.g., unique constraint violations).
        """
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": "Database integrity error: Possible duplicate or invalid data."},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Handle any uncaught exceptions (generic fallback).
        """
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred. Please contact support."},
        )
