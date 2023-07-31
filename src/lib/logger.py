import logging

from .config import Config

conf = Config().get("logger")
logger = logging.getLogger(conf.get("name"))


def setup_logger():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-4s] %(message)s",
        level=conf.get("level", logging.INFO),
        datefmt="%d-%m-%Y %H:%M:%S",
    )
