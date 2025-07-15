#!/bin/bash
# Collect static files
#echo "Collect static files"
#python3 manage.py collectstatic --noinput
# set -e
# echo "Preparing database migrations"
# python3 manage.py makemigrations
echo "Applying database migrations 2"
python3 manage.py migrate --no-input
if [ "$DJANGO_DEBUG" = "true" ]
then
    echo "Running Django in debug mode"
    python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
else
   echo "Running Django in production mode"
   exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
   echo "Running Django in production mode"
fi
