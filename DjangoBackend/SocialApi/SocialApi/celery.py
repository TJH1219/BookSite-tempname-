import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialApi.settings')

app = Celery('SocialApi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'cleanup-expired-tokens': {
        'task': 'api.tasks.cleanup_expired_tokens',
        'schedule': 86400.0
    }
}