import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery('our_book')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r'.format(self.request))

app.conf.update(
    CELERY_TIMEZONE='Asia/Seoul',
    CELERYBEAT_SCHEDULE={
        'send_email_overdue_notification': {
            'task': 'accounts.tasks.send_email_overdue_notification',
            'schedule': crontab(minute=0, hour=11),
            'args': ()
        },
        'send_email_duedate_notification': {
            'task': 'accounts.tasks.send_email_return_date_notification',
            'schedule': crontab(minute=0, hour=15),
            'args': ()
        }
    }
)
