from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    
    # Periodic tasks
    celery.conf.beat_schedule = {
        'send-inactive-user-emails': {
            'task': 'app.tasks.email_tasks.send_inactive_user_reminders',
            'schedule': crontab(hour=10, minute=0),  # Daily at 10 AM
        },
    }
    
    return celery

# In your Flask app initialization
# celery = make_celery(app)