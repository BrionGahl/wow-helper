import datetime
import logging
from logging import Logger


def version() -> str:
    return "v0.0.1"


def config_version() -> str:
    return "0.1"


def time() -> datetime:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logging_handler = logging.StreamHandler()
    logging_handler.setLevel(logging.DEBUG)
    logging_handler.setFormatter(logging.Formatter(f'\x1b[1;30m{time()}\x1b[1;39m %(levelname)-8s \x1b[1;35m%(name)s \x1b[1;39m%(message)s'))
    logger.addHandler(logging_handler)

    return logger
