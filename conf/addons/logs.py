import os


def get_logs_settings(logs_dir: str):
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "[%(asctime)s] %(levelname)s %(message)s - %(pathname)s#lines-%(lineno)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(logs_dir, "default.log"),
                "formatter": "standard",
                "maxBytes": 104857600,
            },
            "handler_error": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": os.path.join(logs_dir, "error.log"),
            },
            "daily_error": {
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(logs_dir, "daily_error.log"),
                "when": "midnight",
                "backupCount": 7,
                "formatter": "standard",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["handler_error", "daily_error"],
                "level": "ERROR",
                "propagate": True,
            },
            "": {
                "handlers": ["default", "daily_error"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }
    return LOGGING
