"""
Logging configuration for the MES application.
"""

import logging
from logging.config import dictConfig

def configure_logging():
    """Configure logging for the application."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(levelname)s: %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO"
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "mes.log",
                "formatter": "detailed",
                "level": "DEBUG"
            }
        },
        "loggers": {
            "mes": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            },
            "sqlalchemy.engine": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": False
            }
        }
    }
    dictConfig(logging_config)

logger = logging.getLogger("mes")
