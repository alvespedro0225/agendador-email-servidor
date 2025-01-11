import schedule
import time
from server_logic.server_logic import RequestHandler
from socketserver import TCPServer
from threading import Thread
from utils.db_handling import DBHandler
from configparser import ConfigParser
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config/config.ini"


def start_server():
    print("Started Server")
    with TCPServer((HOST, PORT), RequestHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n Shutting down")
        finally:
            thread = Thread(target=server.shutdown())
            thread.start()
            print("Closed Server")


def db_management():
    DBHandler.get_data()
    DBHandler.schedule_appointments()


def start_scheduler():
    try:
        print("Started Scheduler")
        while True:
            db_management()
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("")
        print("Shutting down scheduler")
    finally:
        print("Remaining jobs:", schedule.get_jobs())


if __name__ == "__main__":
    config = ConfigParser()
    config.read(CONFIG_PATH)
    PORT = int(config.get("SERVER", "port"))
    HOST = config.get("SERVER", "host")
    try:
        thread1 = Thread(target=start_server)
        thread2 = Thread(target=start_scheduler)
        thread1.start()
        thread2.start()
    except KeyboardInterrupt:
        print("Shutting down.")
