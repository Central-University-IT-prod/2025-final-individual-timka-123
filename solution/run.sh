#!/bin/sh

cd ads_platform
python manage.py migrate
exec python manage.py runserver REDACTED:8080