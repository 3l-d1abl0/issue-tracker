from __future__ import absolute_import
from new_celery.celery import app
from new_celery.email import send_email
from celery.utils.log import get_task_logger
import time
from logger import logger

#logger = get_task_logger(__name__)

@app.task(name="send_email_task")
def send_email_task(email_address, subject, body):
    #logger.info("Sening Email")
    try:
        return send_email(email_address, subject, body)
    except Exception as e:
        logger.debug(e)
        return e
