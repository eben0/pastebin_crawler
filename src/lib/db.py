import os
import threading
import typing

from typing import List, Dict

import arrow
from arrow import Arrow
from tinydb import TinyDB, Query

from .logger import logger
from .config import Config


class DB:
    __instance = None

    def __init__(self) -> None:
        """Initializes the database."""
        self.config = Config().get("db")
        logger.info("Connecting to DB")
        self.create_db()
        self.db = TinyDB(self.config.get("file"))
        self.table = self.db.table(self.config.get("table"))
        self.locks = {}

    def lock(self, fn) -> threading.Lock:
        if fn not in self.locks:
            self.locks[fn] = threading.Lock()
        return self.locks[fn]

    @staticmethod
    def get_instance():
        if DB.__instance is None:
            DB.__instance = DB()
        return DB.__instance

    def create_db(self) -> None:
        """Creates a database file if it doesn't exist."""
        db_dir = os.path.dirname(self.config.get("file"))
        if not os.path.isdir(db_dir):
            os.mkdir(db_dir)

    def insert_pastes(self, pastes: List[Dict]) -> None:
        """Inserts a list of pastes into the database."""
        self.lock("insert_pastes").acquire()
        self.table.insert_multiple(pastes)
        self.lock("insert_pastes").release()

    def insert(self, paste: Dict) -> None:
        """Inserts a  paste dict into the database."""
        self.table.insert(paste)

    def get_all(self) -> List[Dict]:
        """Queries the database for all pastes."""
        return self.table.all()

    def count_by_id(self, paste_id: str) -> int:
        """Counts the database for pastes by id"""
        self.lock("count_by_id").acquire()
        res = self.table.count(Query().id == paste_id)
        self.lock("count_by_id").release()
        return res

    def get_by_id(self, paste_id: str) -> Dict:
        """Queries the database for pastes by id"""
        self.lock("get_by_id").acquire()
        res = self.table.search(Query().id == paste_id)[0]
        self.lock("get_by_id").release()
        return res

    def get_by_author(self, author: str) -> List[Dict]:
        """Queries the database for pastes by author"""
        return self.table.search(Query().author == author)

    def get_by_date(self, from_date: Arrow, to_date: Arrow) -> List[Dict]:
        """Queries the database for pastes by date range"""
        q = Query()
        return self.table.search(
            (q.date >= from_date) & (arrow.get(q.date) <= to_date)
        )


DB.__instance = None
