import logging
import logging.config

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
}

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger()
