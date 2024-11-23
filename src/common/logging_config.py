import os
import logging
import logging.config


def setup_logging(base_dir):
    # Define the log file path using the provided base directory
    log_file_path = os.path.join(base_dir, 'app.log')

    # Update the logging configuration dictionary
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG',
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'level': 'INFO',
                'filename': log_file_path,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }

    # Configure logging
    logging.config.dictConfig(logging_config)

# # Example usage:
# setup_logging(os.path.dirname(__file__))
