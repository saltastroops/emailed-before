import sqlite3
from datetime import datetime
from emailedbefore import SentEmails
from pathlib import Path


def _fetch_rows(sqlite_file: Path):
    connection = sqlite3.connect(
        sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cursor = connection.cursor()
    cursor.execute('SELECT address, topic, sent_at as "s [timestamp]" FROM sent_emails')
    return cursor.fetchall()


def test_register_sent_email(database_file: Path):
    sent_emails = SentEmails(database_file)

    address = "test@example.com"
    topic = "Pay invoice 123"
    sent_at = datetime(2020, 9, 15, 12, 55, 17, 0)

    sent_emails.register(address=address, topic=topic, sent_at=sent_at)

    rows = _fetch_rows(database_file)
    assert len(rows) == 1
    assert set(rows[0]) == {address, topic, sent_at}


def test_an_empty_list_is_returned_if_database_is_empty(database_file: Path):
    sm = SentEmails(database_file)

    ts = sm.sent_at("someone@somewhere.com", "Something")
    assert len(list(ts)) == 0


def test_an_empty_list_is_returned_if_no_email_has_been_sent_for_address(
    database_file: Path,
):
    sm = SentEmails(database_file)
    sm.register("someone@somewhere.com", "Something", datetime(2020, 1, 1, 0, 0, 0, 0))

    ts = sm.sent_at("someone-else@somewhere.com", "Something")
    assert len(list(ts)) == 0


def test_an_empty_list_is_returned_if_no_email_has_been_sent_for_topic(
    database_file: Path,
):
    sm = SentEmails(database_file)
    sm.register("someone@somewhere.com", "Something", datetime(2020, 1, 1, 0, 0, 0, 0))

    ts = sm.sent_at("someone@somewhere.com", "Something else")
    assert len(list(ts)) == 0


def test_only_the_requested_address_and_topic_are_considered(database_file: Path):
    sm = SentEmails(database_file)

    data = [
        {
            "address": "someone@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 9, 15, 17, 0, 0),
        },
        {
            "address": "someone_else@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 9, 15, 18, 0, 0),
        },
        {
            "address": "someone@somewhere.com",
            "topic": "Something else",
            "sent_at": datetime(2020, 9, 15, 19, 0, 0),
        },
        {
            "address": "someone@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 10, 15, 17, 0, 0),
        },
        {
            "address": "someone-else@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 10, 15, 18, 0, 0),
        },
        {
            "address": "someone@somewhere.com",
            "topic": "Something else",
            "sent_at": datetime(2020, 10, 15, 19, 0, 0),
        },
    ]

    for d in data:
        sm.register(**d)

    ts = sm.sent_at(address=data[0]["address"], topic=data[0]["topic"])
    assert ts == [data[0]["sent_at"], data[3]["sent_at"]]


def test_the_same_datetime_can_occur_more_than_once(database_file):
    sm = SentEmails(database_file)

    sm.register(
        address="someone@somewhere.com",
        topic="Something",
        sent_at=datetime(2020, 7, 31, 9, 14, 8),
    )
    sm.register(
        address="someone@somewhere.com",
        topic="Something",
        sent_at=datetime(2020, 7, 31, 9, 14, 8),
    )
    sm.register(
        address="someone@somewhere.com",
        topic="Something",
        sent_at=datetime(2020, 7, 31, 9, 14, 8),
    )

    ts = sm.sent_at(address="someone@somewhere.com", topic="Something")
    assert len(list(ts)) == 3


def test_sent_emails_are_returned_ordered_by_datetime(database_file: Path):
    sm = SentEmails(database_file)

    ordered_times = [
        datetime(2019, 7, 5, 12, 0, 0, 0),
        datetime(2020, 1, 1, 0, 0, 0, 0),
        datetime(2020, 1, 1, 0, 0, 0, 1),
        datetime(2020, 1, 1, 0, 0, 0, 2),
        datetime(2020, 1, 1, 0, 15, 0, 1),
        datetime(2020, 1, 14, 0, 7, 0, 1),
        datetime(2020, 9, 1, 0, 15, 0, 1),
        datetime(2021, 1, 1, 0, 0, 0, 1),
    ]
    unordered_times = [
        ordered_times[3],
        ordered_times[2],
        ordered_times[7],
        ordered_times[5],
        ordered_times[6],
        ordered_times[0],
        ordered_times[1],
        ordered_times[4],
    ]

    address = "someone@somewhere.com"
    topic = "Something"
    for t in unordered_times:
        sm.register(address=address, topic=topic, sent_at=t)

    ts = sm.sent_at(address=address, topic=topic)
    assert ts == ordered_times


def test_last_sent_at_returns_none_if_never_sent(database_file: Path):
    sm = SentEmails(database_file)

    t = sm.last_sent_at(address="someone@somewhere.comn", topic="Something")
    assert t is None


def test_last_sent_at_returns_datetime_when_last_sent(database_file: Path):
    sm = SentEmails(database_file)

    data = [
        {
            "address": "someone@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 4, 6, 0, 0, 0),
        },
        {
            "address": "someone@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 4, 8, 0, 0, 0),
        },
        {
            "address": "someone@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 4, 7, 0, 0, 0),
        },
        {
            "address": "someone-else@somewhere.com",
            "topic": "Something",
            "sent_at": datetime(2020, 4, 9, 0, 0, 0),
        },
    ]
    for d in data:
        sm.register(address=d["address"], topic=d["topic"], sent_at=d["sent_at"])

    t = sm.last_sent_at(address="someone@somewhere.com", topic="Something")
    assert t == data[1]["sent_at"]


def test_database_table_is_not_recreated(database_file: Path):
    sm = SentEmails(database_file)
    sm.register(
        address="someone@somewhere.comn",
        topic="Something",
        sent_at=datetime(2019, 5, 3, 23, 45, 56),
    )

    sm2 = SentEmails(database_file)

    ts = sm2.sent_at(address="someone@somewhere.comn", topic="Something")
    assert len(list(ts)) == 1
