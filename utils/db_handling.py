import datetime
import schedule
import asyncio
from .utils import Appointment, connect_db
from .mail_handling import MailHandler
from pathlib import Path
from pydantic import BaseModel
from typing import ClassVar


class DBHandler(BaseModel):

    appointed: ClassVar[list[Appointment]] = []
    new_appoints: ClassVar[list[Appointment]] = []
    db_path: ClassVar[Path] = Path(__file__).parent.parent / "data/appointments.sqlite3"

    @classmethod
    def get_data(
        cls,
        time: datetime.time = datetime.datetime.now().time(),
        today: datetime.date = datetime.date.today(),
    ):
        time_str: str = str(time.replace(second=00, microsecond=0))
        with connect_db(cls.db_path) as cursor:
            data = cursor.execute(
                f"select * from appointments where send_date='{today}' and send_time>'{time_str}'"
            )
            for row in data:
                new_appoint = Appointment(
                    reciever=row[0], send_time=row[2], subject=row[3], message=row[4]
                )
                if new_appoint not in cls.appointed:
                    cls.new_appoints.append(new_appoint)

    @classmethod
    def schedule_appointments(cls):
        sent = False
        for appoint in cls.new_appoints:
            appointed = (
                schedule.every()
                .day.at(f"{appoint.hour}:{appoint.mins}")
                .do(asyncio.run, MailHandler.send_mail(appoint))
            )
            print(
                f'"{appoint.message} for {appoint.reciever}" scheduled for {appointed.next_run}'
            )
            cls.appointed.append(appoint)
            sent = True
        if sent:
            print("")
        cls.new_appoints = []
