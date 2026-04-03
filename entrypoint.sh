#!/bin/sh

set -e

python manage.py migrate

exec gunicorn athletics_site.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3
