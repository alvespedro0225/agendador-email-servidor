import sqlite3
from contextlib import contextmanager
from pydantic import BaseModel
from typing import Any, Optional

class Appointment(BaseModel):

    reciever: str
    send_time: str
    subject: str
    message: str
    mins: Optional[str] = None
    hour: Optional[str] = None

    def model_post_init(self, __context: Any) -> None:
        self.hour = self.send_time[:2]
        self.mins = self.send_time[3:5]
        return super().model_post_init(__context)


@contextmanager
def connect_db(path):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    try:
        yield cursor
    finally:
        db.close()
