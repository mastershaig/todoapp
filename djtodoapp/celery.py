from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os, logging
from django.conf import settings

logger = logging.getLogger("Celery")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djtodoapp.settings')

app = Celery('djtodoapp')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.update(
    BROKER_URL='redis://localhost:6379/0',
    CELERYBEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
    CELERY_RESULT_BACKEND='redis://localhost:6379/1',
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_ACCEPT_CONTENT=['json', ],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)
#

# app.conf.beat_schedule = {
#     'every_week_update_leaderboard': {
#         'task': 'travel.tasks.image_convert_to_right_format',
#         'schedule': crontab(hour=0, minute=1),
#     },
# }
