import logging
import logging.config
import os

# Define the log file path
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'app.log')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Handler to print to console
            'formatter': 'standard',
            'level': 'DEBUG',  # Print debug and above to console
        },
        'file': {
            'class': 'logging.FileHandler',  # Handler to write to log file
            'formatter': 'standard',
            'level': 'INFO',  # Write info and above to log file
            'filename': LOG_FILE_PATH,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],  # Send logs to both console and file
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
