import logging

logger = logging.getLogger()

handler = logging.StreamHandler()
formatter = logging.Formatter('\033[1m[%(levelname)s]\033[0m: %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

WARNING = logging.WARNING
ERROR = logging.ERROR
DEBUG = logging.DEBUG
INFO = logging.INFO

levels = {
    'warning': WARNING,
    'error': ERROR,
    'info': INFO,
    'debug': DEBUG
}

def setLevel(level):
    if level in levels:
        logger.setLevel(levels[level])

def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)

setLevel(ERROR)