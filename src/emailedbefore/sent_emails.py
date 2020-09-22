import os
import sqlite3
from datetime import datetime
from typing import Any, List, Optional, Union


class SentEmails:
    """
    A class for registering sent emails and querying when emails have been sent.

    The information is stored in a Sqlite3 database, whose file must be passed to the
    constructor. The required table in that database is created automatically.

    Parameters
    ----------
    sqlite_file : path-like object
        The file containing the Sqlite3 database.

    """

    def __init__(self, sqlite_file: Union[str, "os.PathLike[Any]"]):
        self.connection = sqlite3.connect(
            sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self._create_table()
        self._create_address_index()
        self._create_topic_index()
        self._create_sent_at_index()

    def register(self, address: str, topic: str, sent_at: datetime) -> None:
        """
        Register the fact that a email about a topic has been sent to an address at a
        given datetime.

        Parameters
        ----------
        address : str
            Email address.
        topic : str
            Topic.
        sent_at : datetime
            Datetime when the email was sent.

        """

        sql = """\
INSERT INTO sent_emails (address, topic, sent_at)
       VALUES (?, ?, ?)
        """
        with self.connection:
            params = (address, topic, sent_at)
            self.connection.execute(sql, params)

    def sent_at(self, address: str, topic: str) -> List[datetime]:
        """
        The datetimes when an email about a topic has been sent to an address.

        The list of datetimes is returned in ascending order.

        Parameters
        ----------
        address : str
            Email address.
        topic : str
            Topic.

        Returns
        -------
        list
            Datetimes when an email was sent.

        """

        sql = """\
SELECT sent_at AS "s [timestamp]"
FROM sent_emails
WHERE address=? AND topic=?
ORDER BY sent_at
"""
        cursor = self.connection.cursor()
        cursor.execute(sql, (address, topic))
        return [row[0] for row in cursor.fetchall()]

    def last_sent_at(self, address: str, topic: str) -> Optional[datetime]:
        """
        The datetime when an emil about a topic was sent to an address.

        None is returned if no such email has ever been sent.

        Parameters
        ----------
        address : str
            Email address.
        topic : str
            Topic.

        Returns
        -------
        datetime
            The datetime when an email was last sent.

        """

        sent_at = list(self.sent_at(address=address, topic=topic))
        if len(sent_at) == 0:
            return None
        return sent_at[-1]

    def _create_table(self) -> None:
        sql = """\
CREATE TABLE IF NOT EXISTS sent_emails (
  address TEXT NOT NULL,
  topic TEXT NOT NULL,
  sent_at TEXT NOT NULL
)
        """

        with self.connection:
            self.connection.execute(sql)

    def _create_address_index(self) -> None:
        sql = """\
CREATE INDEX IF NOT EXISTS idx_address ON sent_emails (address)
        """
        with self.connection:
            self.connection.execute(sql)

    def _create_topic_index(self) -> None:
        sql = """\
CREATE INDEX IF NOT EXISTS idx_topic ON sent_emails (topic)
        """
        with self.connection:
            self.connection.execute(sql)

    def _create_sent_at_index(self) -> None:
        sql = """\
CREATE INDEX IF NOT EXISTS idx_sent_at ON sent_emails (sent_at)
        """
        with self.connection:
            self.connection.execute(sql)
