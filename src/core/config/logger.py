"""Structured logging configuration."""
import logging
import logging.config
import json
from contextvars import ContextVar
from .settings import settings

# Context variable to hold the correlation ID per request
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

class JSONFormatter(logging.Formatter):
    """Formatter for JSON output in production."""
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "correlation_id": correlation_id.get(),
            "timestamp": self.formatTime(record, self.datefmt)
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

class ConsoleFormatter(logging.Formatter):
    """Formatter for human-readable output in development."""
    def format(self, record: logging.LogRecord) -> str:
        corr_id = correlation_id.get()
        corr_str = f" [{corr_id}]" if corr_id else ""
        log_message = f"{self.formatTime(record, self.datefmt)} - {record.levelname} - {record.name}{corr_str} - {record.getMessage()}"
        if record.exc_info:
            log_message += f"\n{self.formatException(record.exc_info)}"
        return log_message

def setup_logging() -> None:
    """Configure logging system-wide."""
    formatter = "json" if settings.ENVIRONMENT == "prod" else "console"
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JSONFormatter,
            },
            "console": {
                "()": ConsoleFormatter,
            },
        },
        "handlers": {
            "default": {
                "formatter": formatter,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": settings.LOG_LEVEL,
            },
            # Silence noisy libraries
            "uvicorn.access": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "aiomqtt": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(logging_config)
