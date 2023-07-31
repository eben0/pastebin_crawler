from lib.logger import setup_logger, logger
from lib.executor import CrawlerExecutor

# Set up logger
setup_logger()

# let's start
logger.info("Starting Pastebin Crawler")
CrawlerExecutor().run()
