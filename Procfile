web: python manage.py collectstatic --noinput; gunicorn_django --bind=0.0.0.0:$PORT alexandria/settings/heroku.py
worker: python manage.py celery worker --loglevel=info