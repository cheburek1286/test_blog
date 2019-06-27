#!/bin/sh
source venv/bin/activate
flask db upgrade
pybabel compile -d app/translations
exec gunicorn -b :5000 --access-logfile - --error-logfile - main:app