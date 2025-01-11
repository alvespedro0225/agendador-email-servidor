from socketserver import BaseRequestHandler
from .utils import connect_db
from pathlib import Path


class RequestHandler(BaseRequestHandler):

    db_path = Path(__file__).parent.parent / "data" / "appointments.sqlite3"
    delimiter = "ṕ"
    formatting = "UTF-8"

    def handle(self):
        request = str(self.request.recv(4096), self.formatting)
        keys = ["email", "send_date", "send_time", "subject", "message"]
        values = []
        start = 0
        size = len(request)
        for index in range(size):
            if request[index] == self.delimiter:
                values.append(request[start:index])
                start = index + 1
        for key, value in zip(keys, values):
            setattr(self, key, value)
        self.db_write()

    def db_write(self):
        with connect_db(self.db_path) as cursor:
            cursor.execute(
                f"insert into appointments values('{self.email}','{self.send_date}','{self.send_time}','{self.subject}','{self.message}');"
            )
            print("Appointment scheduled.")
