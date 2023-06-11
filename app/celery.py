from datetime import timedelta

from celery import Celery

from app.config import Config
from app.services.metrics.loader import MetricsLoader
from app.services.metrics.tmp_checker import check_tpm_metrics

app = Celery('tasks', broker=Config.redis_url)


@app.task
def save_metrics():
    MetricsLoader()


@app.task
def check_tmp():
    check_tpm_metrics()


app.conf.beat_schedule = {
    'load_metrics': {
        'task': 'app.celery.save_metrics',
        'schedule': timedelta(minutes=Config.api_read_period),
    },
    'check_tmp': {
        'task': 'app.celery.save_metrics',
        'schedule': timedelta(minutes=Config.tmp_read_period),
    },
}

if __name__ == '__main__':
    app.start()
