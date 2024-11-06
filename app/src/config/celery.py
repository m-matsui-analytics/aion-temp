import os

from celery import Celery
from dotenv import load_dotenv


load_dotenv()
DJANGO_ENV = os.getenv("DJANGO_ENV")
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"config.settings.{DJANGO_ENV}")


app = Celery('config')
# 基本的な設定を先に行う
# app.conf.update(
#     worker_state_db=None,
#     # 他の設定があれば追加
# )
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.worker_state_db=None

# Django設定を適用
import django
django.setup()


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

from tasks.tasks.mail_gen_data_registerer import MailGenDataRegisterer
from tasks.tasks.content_anaysis_result_registerer import ContentAnalysisResultRegisterer

app.register_task(MailGenDataRegisterer())
app.register_task(ContentAnalysisResultRegisterer())

# app.register_task(MailGenDataRegisterer(), name=MailGenDataRegisterer.name)
# 
