#!/bin/sh

set -e

while ! nc -z db 5432; do
  sleep 1
done

python manage.py migrate

exec gunicorn athletics_site.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3
