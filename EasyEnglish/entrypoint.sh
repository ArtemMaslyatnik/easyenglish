#!/bin/bash
# Collect static files
#echo "Collect static files"
#python3 manage.py collectstatic --noinput
# set -e
# echo "Preparing database migrations"
# python3 manage.py makemigrations
echo "Applying database migrations 2"
python3 manage.py migrate --no-input
echo "Starting server."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3