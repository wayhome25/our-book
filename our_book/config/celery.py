import os
from celery import Celery
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
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'say_hello-every-seconds': {
            'task': 'accounts.tasks.say_hello_every_seconds',
            'schedule': timedelta(seconds=1),
            'args': ()
        },
    }
)
