from __future__ import absolute_import
from new_celery.celery import app
from new_celery.email import send_email
from celery.utils.log import get_task_logger
import time

#logger = get_task_logger(__name__)

@app.task(name="send_email_task")
def send_email_task(email_address, subject, body):
    #logger.info("Sening Email")
    return send_email(email_address, subject, body)
'''
def longtime_add(x, y):
    print 'long time task begins'
    # sleep 5 seconds
    time.sleep(5)
    print 'long time task finished'
    return x + y
'''
