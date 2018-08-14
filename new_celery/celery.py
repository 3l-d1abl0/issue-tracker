from __future__ import absolute_import
from celery import Celery

app = Celery('new_celery', broker='redis://localhost:6379/0',include=['new_celery.tasks'])
