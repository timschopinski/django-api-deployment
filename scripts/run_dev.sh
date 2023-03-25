#!/bin/sh

set -e
echo 'Waiting for postgres...'
python manage.py wait_for_db
echo 'PostgreSQL started'

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

gunicorn app.wsgi:application --bind 0.0.0.0:8000