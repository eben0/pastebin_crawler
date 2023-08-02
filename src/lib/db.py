import os

from typing import List, Dict

import arrow
from arrow import Arrow
from tinydb import TinyDB, Query

from .logger import logger
from .config import Config
from .tools import synchronized


class DB:
    __instance = None

    def __init__(self) -> None:
        """Initializes the database."""
        self.config = Config.instance().get("db")
        logger.info("Connecting to DB")
        self.create_db()
        self.db = TinyDB(self.config.get("file"))
        self.table = self.db.table(self.config.get("table"))

    @staticmethod
    def instance():
        if DB.__instance is None:
            DB.__instance = DB()
        return DB.__instance

    def create_db(self) -> None:
        """Creates a database file if it doesn't exist."""
        db_dir = os.path.dirname(self.config.get("file"))
        if not os.path.isdir(db_dir):
            os.mkdir(db_dir)

    @synchronized
    def insert_pastes(self, pastes: List[Dict]) -> None:
        """Inserts a list of pastes into the database."""
        self.table.insert_multiple(pastes)

    @synchronized
    def insert(self, paste: Dict) -> None:
        """Inserts a  paste dict into the database."""
        self.table.insert(paste)

    @synchronized
    def get_all(self) -> List[Dict]:
        """Queries the database for all pastes."""
        return self.table.all()

    @synchronized
    def count_by_id(self, paste_id: str) -> int:
        """Counts the database for pastes by id"""
        return self.table.count(Query().id == paste_id)

    @synchronized
    def get_by_id(self, paste_id: str) -> Dict:
        """Queries the database for pastes by id"""
        return self.table.search(Query().id == paste_id)[0]

    @synchronized
    def get_by_author(self, author: str) -> List[Dict]:
        """Queries the database for pastes by author"""
        return self.table.search(Query().author == author)

    @synchronized
    def get_by_date(self, from_date: Arrow, to_date: Arrow) -> List[Dict]:
        """Queries the database for pastes by date range"""
        q = Query()
        return self.table.search(
            (q.date >= from_date) & (arrow.get(q.date) <= to_date)
        )


DB.__instance = None
