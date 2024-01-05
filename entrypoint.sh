#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
celery -A navya_project worker --loglevel=info &
celery -A navya_project beat --loglevel=info &
echo "================================ Server is starting now  =================================="
gunicorn --bind 0.0.0.0:8000 --reload navya_project.wsgi &

trap 'kill -TERM $PID_CELERY $PID_GUNICORN' TERM INT

PID_CELERY=$!
PID_GUNICORN=$!

wait $PID_CELERY $PID_GUNICORN

trap - TERM INT
wait $PID_CELERY $PID_GUNICORN
