from lib.logger import logger, setup_logger
from lib.pastebin_crawler import PastebinCrawler

# Set up logger
setup_logger()

# let's start
logger.info("Starting Pastebin Crawler")
crawler = PastebinCrawler()
crawler.run()
