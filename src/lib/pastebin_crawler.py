import os.path
from typing import List, Dict, Union
from concurrent.futures import ThreadPoolExecutor, Future

import requests
import arrow
from lxml import etree

from .config import Config
from .constants import DEFAULT_INTERVAL
from .db import DB
from .logger import logger
from .paste import Paste


class PastebinCrawler:
    def __init__(self) -> None:
        self.db = DB.instance()
        self.config = Config.instance().get("crawler")
        self.pool = ThreadPoolExecutor()
        self.interval = self.config.get("interval", DEFAULT_INTERVAL)

    def crawl(self) -> List[Dict]:
        """
        crawls the website and extract pastes
        """
        pastes = []
        links = self._crawl_home()

        # we'll go over the links and extract the paste details
        futures: List[Future] = []
        for link in links:
            futures.append(self.pool.submit(self._crawl_to_link, link))

        for future in futures:
            paste = future.result()
            if paste is None:
                continue
            # add the paste to the list
            pastes.append(paste.to_dict())
            # save it to a file
            self.save_to_file(paste)

        if len(pastes) > 0:
            self._store_crawls(pastes)

        return pastes

    def _store_crawls(self, pastes: List[Paste]):
        # insert the pastes details to the database
        len_pastes = len(pastes)
        if len_pastes > 0:
            self.db.insert_pastes(pastes)
            logger.info(f"Inserted {len_pastes} pastes into the database.")
        else:
            logger.info("No pastes inserted into the database.")

    def _crawl_home(self) -> List:
        base_url = self.config.get("url")
        logger.info(f"Crawling {base_url}...")

        # getting recent pastes from the homepage
        tree = self.scrap(base_url)
        # find pastes from the sidebar meny
        sidebar = tree.xpath('//ul[@class="sidebar__menu"]')[0]

        # getting the link element
        links = sidebar.xpath(".//a")
        logger.info(f"Found {len(links)} pastes")
        logger.debug("links: %s", links)
        return links

    def _crawl_to_link(self, link) -> Union[Paste, None]:
        href = link.get("href")
        paste_id = href.replace("/", "")  # ID is a stripped href
        exising_paste = self.db.count_by_id(paste_id) > 0

        # checking for existing pastes in the DB
        if exising_paste:
            logger.info(f"paste '{paste_id}' already exists. Skipping")
            return None
        else:
            logger.info(f"Scraping paste '{paste_id}'")

        # scarping the paste url
        base_url = self.config.get("url")
        paste_url = base_url + href
        paste_tree = self.scrap(paste_url)

        # create the Paste model
        paste = Paste()
        paste.set_id(paste_id)

        # extract title
        title_el = paste_tree.xpath("//title")[0]
        if title_el is not None:
            paste.set_title(self.normalize_title(title_el.text))

        # extract author
        author_el = paste_tree.xpath('//div[@class="username"]//a')[0]
        if author_el is not None:
            paste.set_author(self.normalize_author(author_el.text))

        # extract date
        date_el = paste_tree.xpath('//div[@class="date"]//span')[0]
        if date_el is not None:
            paste.set_date(self.normalize_date(date_el.get("title")))

        # getting the content by calling the /raw url
        raw_url = f"{base_url}/raw/{paste.id}"
        content = self.scrap(raw_url, to_text=True)
        if content:
            paste.set_content(content.strip())
        return paste

    def save_to_file(self, paste: Paste) -> None:
        """
        save the content to a file
        :param paste: the paste model
        """
        # creating the directory if it doesn't exist
        pastes_path = self.config.get("pastes_path")
        if not os.path.isdir(pastes_path):
            os.mkdir(pastes_path)
        paste_path = f"{pastes_path}/{paste.id}.txt"
        with open(paste_path, "w", encoding="utf-8") as f:
            f.write(paste.content)
            f.close()

    def normalize_date(self, date_string: str) -> str:
        """
        parsing date
        :param date_string: pastebin's date string
        :return: normalized date
        """
        date_string = date_string.strip().replace(
            "CDT", "America/Chicago"
        )  # replacing CDT with timezone because arrow can't parse it
        date_format = "dddd Do [of] MMMM YYYY h:mm:ss A ZZZ"
        return str(arrow.get(date_string, date_format).to("utc"))

    def normalize_author(self, author: str) -> str:
        """
        check for author name and return Unknown
        if it's not a registered user
        :param author: the author name
        :return: normalized author name
        """
        author = author.strip()
        normalize_values = ["", "Unknown", "Anonymous", "A Guest"]
        default = normalize_values[-1]  # default is "A Guest"
        if author in normalize_values:
            return default
        return author

    def normalize_title(self, title: str) -> str:
        """
        normalizing the title
        :param title: the author name
        :return: normalized author name
        """
        normalize_values = ["", "Unknown", "Untitled"]
        # strip out the url
        title = title.strip().replace(" - Pastebin.com", "")
        default = normalize_values[-1]  # default is "Untitled"
        if title in normalize_values:
            return default
        return title

    def get_pastes(self) -> List[Dict]:
        """
        get all pastes from the database
        :return: list of pastes
        """
        return self.db.get_all()

    def scrap(self, url: str, to_text=False) -> Union[etree.HTML, str]:
        """
        fetched and parsed url into HTML tree
        :param url: url to fetch
        :return: HTML Tree
        """
        # fetching the url
        html: etree.HTML
        paste_response = requests.get(url)
        if paste_response.status_code >= 400:
            logger.warning(f"Failed to fetch {url}")
            logger.error(paste_response)
            return etree.HTML("")
        elif to_text:
            return paste_response.text
        # parsing the HTML
        return etree.HTML(paste_response.content)
