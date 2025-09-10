#!/bin/sh
python manage.py makemigrations accounts catalog orders profiles recommendations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py create_default_superuser
python manage.py seed

exec "$@"