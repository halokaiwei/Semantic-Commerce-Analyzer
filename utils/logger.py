import os
import logging

def get_logger(name=None):
    log_path = os.path.join(os.path.dirname(__file__), 'crawler.log')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        logger.addHandler(file_handler)

    return logger
