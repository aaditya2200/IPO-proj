from redis_conf import RedisConf
from celery import Celery
from celery.schedules import crontab

app = Celery()

