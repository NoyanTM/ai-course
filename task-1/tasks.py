import os
from datetime import datetime, timedelta

from dotenv import load_dotenv, find_dotenv
from celery import Celery
from celery.schedules import crontab

from main import parse_data

load_dotenv(find_dotenv())

REDIS_URL = f"redis://:{os.getenv("REDIS_PASSWORD")}@{os.getenv("REDIS_HOST")}:{os.getenv('REDIS_PORT')}"

app_celery = Celery("tasks", broker=f'{REDIS_URL}/0', backend=f"{REDIS_URL}/1")


@app_celery.task(name="tasks.execute_parsing")
def execute_parsing():
    parse_data()


app_celery.conf.beat_schedule = {
    'execute-parsing-every-24-hours': {
        'task': "tasks.execute_parsing",
        'schedule': crontab(minute=0, hour=21), # timedelta(hours=24)
    },
}
app_celery.conf.timezone = 'UTC'
