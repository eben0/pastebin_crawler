from lib.logger import Logger
from lib.executor import CrawlerExecutor

# Set up logger
Logger.setup()

# let's start
Logger.logger().info("Starting Pastebin Crawler")
CrawlerExecutor().run()
