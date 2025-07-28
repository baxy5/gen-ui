import logging
from typing import Optional

_loggers = {}


def get_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a reusable logger instance with the specified name and level.
    If called multiple times with the same name, returns the same logger.
    """
    global _loggers
    if name is None:
        name = "genui"
    if name in _loggers:
        return _loggers[name]
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.propagate = False
    _loggers[name] = logger
    return logger
