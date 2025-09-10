#!/bin/sh
set -e  

echo " Starting entrypoint script..."

echo " Running makemigrations..."
python manage.py makemigrations accounts catalog orders profiles recommendations --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo " Creating default superuser..."
python manage.py create_default_superuser || echo " Skipping superuser creation (already exists?)"

echo "Seeding database..."
python manage.py seed || echo " Skipping seeding (already done?)"

echo "Entrypoint setup complete. Starting application..."
exec "$@"
