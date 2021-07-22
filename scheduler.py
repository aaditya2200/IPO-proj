import schedule
import time
from tasks.fetch_and_store import fetch_and_store
from tasks.notify import notify


def task_scheduler():
    fetch_and_store()
    notify()


schedule.every().day.at("21:48").do(task_scheduler)

while True:
    schedule.run_pending()
    time.sleep(1)