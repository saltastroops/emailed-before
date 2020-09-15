import os
import sqlite3
from typing import Union


class SentMails:
    """
    A class for registering sent mails and querying when mails have been sent.

    The information is stored in a Sqlite3 database, whose file must be passed to the
    constructor. The required table in that database is created automatically.

    Parameters
    ----------
    sqlite_file : path-like object
        The file containing the Sqlite3 database. This may be ":memory:" if you require
        a database in RAM instead of on disk, for example in unit tests.

    """
    def __init__(self, sqlite_file: Union[str, os.PathLike]):
        self.connection = sqlite3.connect(sqlite_file)
        self._create_table()
        self._create_address_index()
        self._create_topic_index()
        self._create_sent_at_index()

    def _create_table(self):
        sql = """\
CREATE TABLE IF NOT EXISTS sent_emails (
  address TEXT NOT NULL,
  topic TEXT NOT NULL,
  sent_at TEXT NOT NULL
)
        """

        with self.connection:
            self.connection.execute(sql)

    def _create_address_index(self):
        sql = """\
CREATE INDEX IF NOT EXISTS idx_address ON sent_emails (address)
        """
        with self.connection:
            self.connection.execute(sql)

    def _create_topic_index(self):
        sql = """\
CREATE INDEX IF NOT EXISTS idx_topic ON sent_emails (topic)
        """
        with self.connection:
            self.connection.execute(sql)

    def _create_sent_at_index(self):
        sql = """\
CREATE INDEX IF NOT EXISTS idx_sent_at ON sent_emails (sent_at)
        """
        with self.connection:
            self.connection.execute(sql)
