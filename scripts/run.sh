#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py migrate

gunicorn --workers=3 --threads=6 --worker-class=gthread --worker-tmp-dir /dev/shm app.wsgi