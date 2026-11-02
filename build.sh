#!/usr/bin/env bash
# exit on error
set -o pipefail
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

# Création automatique de votre compte Admin en production si configuré dans Render
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --no-input || true
fi