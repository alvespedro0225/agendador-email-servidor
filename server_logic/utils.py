from contextlib import contextmanager
from pydantic import BaseModel
import sqlite3


class Appointment(BaseModel):

    sender: str
    reciever: str
    subject: str
    message: str
    send_time: str

    def __post_init__(self):
        self.hour = self.send_time[:2]
        self.min = self.send_time[3:5]


@contextmanager
def connect_db(path):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    try:
        yield cursor
    finally:
        db.commit()
        db.close()
