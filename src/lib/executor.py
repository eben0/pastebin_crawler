import traceback

from .pastebin_crawler import PastebinCrawler
from .timer import RepeatTimer
from .logger import logger


class CrawlerExecutor(PastebinCrawler):
    def run(self) -> None:
        """
        this method runs the crawler periodically every X seconds
        """
        RepeatTimer(self.interval, self._runner).run()

    def _runner(self):
        try:
            self.crawl()
            logger.info(f"sleeping for {self.interval} seconds")
        except Exception:
            logger.error("Failed to crawl:\n%s", traceback.format_exc())
