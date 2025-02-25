#!/bin/sh

# Run database migrations
python django_backend/manage.py migrate --noinput

# Start the Django development server
exec python django_backend/manage.py runserver 0.0.0.0:8000
