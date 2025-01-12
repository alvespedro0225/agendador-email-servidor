import sqlite3
from contextlib import contextmanager
from pydantic import BaseModel

@contextmanager
def connect_db(path):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    try:
        yield cursor
    finally:
        db.commit()
        db.close()
