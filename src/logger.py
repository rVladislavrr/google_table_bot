import logging
import sys
from logging import Formatter, StreamHandler


class ColorFormatter(Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    msg = "%(levelname)s:     %(asctime)s - %(name)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + msg + reset,
        logging.INFO: grey + msg + reset,
        logging.WARNING: yellow + msg + reset,
        logging.ERROR: red + msg + reset,
        logging.CRITICAL: bold_red + msg + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_fmt)
        return formatter.format(record)


def setup_logging(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Обработчик для консоли с цветами
    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter())

    logger.addHandler(console_handler)

    return logger
