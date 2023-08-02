import logging

from .config import Config

config = Config.instance().get("logger")
logger = logging.getLogger(config.get("name"))


class Logger:
    @staticmethod
    def logger():
        return logger

    @staticmethod
    def setup():
        logging.basicConfig(
            format="%(asctime)s [%(levelname)-4s] %(message)s",
            level=config.get("level", logging.INFO),
            datefmt="%d-%m-%Y %H:%M:%S",
        )
