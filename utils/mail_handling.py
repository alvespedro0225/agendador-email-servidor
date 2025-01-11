import smtplib
import schedule
import asyncio
from pathlib import Path
from configparser import ConfigParser
from pydantic import BaseModel
from typing import ClassVar
from email.message import EmailMessage

from .utils import Appointment

CONFIG_PATH = Path(__file__).parent.parent / "config/config.ini"
config = ConfigParser()
config.read(CONFIG_PATH)


class MailHandler(BaseModel):

    email: ClassVar[str] = config.get("EMAIL", "email")
    pw: ClassVar[str] = config.get("EMAIL", "pw")
    host: ClassVar[str] = config.get("EMAIL", "host")
    port: ClassVar[int] = int(config.get("EMAIL", "port"))

    @classmethod
    async def send_mail(cls, appoint: Appointment):
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(cls.connect_to_server())
                tg.create_task(cls.create_mail(appoint=appoint))
            cls.server.send_message(cls.message)
            print("Message sent")
            return schedule.CancelJob
        finally:
            cls.server.close()
            print("Server closed", "\n")

    @classmethod
    async def connect_to_server(
        cls,
    ) -> None:

        server = smtplib.SMTP(cls.host, cls.port)
        server.starttls()
        server.login(cls.email, cls.pw)
        print("Login success")
        cls.server = server

    @classmethod
    async def create_mail(cls, appoint: Appointment):
        message = EmailMessage()
        message["to"] = appoint.reciever
        message["subject"] = appoint.subject
        message["from"] = cls.email
        message.set_content(appoint.message)
        print("Message ready")
        cls.message = message
