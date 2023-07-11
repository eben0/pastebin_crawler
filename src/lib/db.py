import os
from typing import List, Dict

import arrow
from arrow import Arrow
from tinydb import TinyDB, Query

from .config import config
from .logger import logger


class DB:
    def __init__(self) -> None:
        """Initializes the database."""
        logger.info("Connecting to DB")
        self.config = config.get("db", {})
        self.create_db()
        self.db = TinyDB(self.config.get("file"))
        self.table = self.db.table(self.config.get("table"))

    def create_db(self) -> None:
        """Creates a database file if it doesn't exist."""
        db_dir = os.path.dirname(self.config.get("file"))
        if not os.path.isdir(db_dir):
            os.mkdir(db_dir)

    def insert_pastes(self, pastes: List[Dict]) -> None:
        """Inserts a list of pastes into the database."""
        self.table.insert_multiple(pastes)

    def insert(self, paste: Dict) -> None:
        """Inserts a  paste dict into the database."""
        self.table.insert(paste)

    def get_all(self) -> List[Dict]:
        """Queries the database for all pastes."""
        return self.table.all()

    def count_by_id(self, paste_id: str) -> int:
        """Counts the database for pastes by id"""
        return self.table.count(Query().id == paste_id)

    def get_by_id(self, paste_id: str) -> Dict:
        """Queries the database for pastes by id"""
        return self.table.search(Query().id == paste_id)[0]

    def get_by_author(self, author: str) -> List[Dict]:
        """Queries the database for pastes by author"""
        return self.table.search(Query().author == author)

    def get_by_date(self, from_date: Arrow, to_date: Arrow) -> List[Dict]:
        """Queries the database for pastes by date range"""
        q = Query()
        return self.table.search(
            (q.date >= from_date) & (arrow.get(q.date) <= to_date)
        )
