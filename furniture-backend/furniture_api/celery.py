# furniture_api/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_api.settings')

app = Celery('furniture_api')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Auto-discover tasks in installed apps
app.autodiscover_tasks()
