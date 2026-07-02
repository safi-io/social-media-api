import logging
import logging.config


class NormalizeLoggerNameFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.name.startswith("uvicorn.error"):
            record.name = "uvicorn"
        return True


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
            "filters": ["normalize_logger_name"],
        },
    },
    "filters": {
        "normalize_logger_name": {
            "()": NormalizeLoggerNameFilter,
        },
    },
    "root": {
        "handlers": ["stdout"],
        "level": "INFO",
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["stdout"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["stdout"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["stdout"],
            "propagate": False,
        },
        "app.request": {
            "level": "INFO",
            "handlers": ["stdout"],
            "propagate": False,
        },
    },
}


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)