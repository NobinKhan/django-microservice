#!/bin/sh
set -e
FILE=/project/.initialized
if [ -f "$FILE" ]; then
    echo "Skipping initialization..."
    echo "If you want to run initialization again remove the file"
    /root/.local/bin/poetry run python manage.py wait_for_db
    /root/.local/bin/poetry run python manage.py runserver 0.0.0.0:8000
else
    echo "first time run"
    /root/.local/bin/poetry run python manage.py wait_for_db
    # /root/.local/bin/poetry run python manage.py makemigrations
    # /root/.local/bin/poetry run python manage.py migrate
    /root/.local/bin/poetry run python manage.py runserver 0.0.0.0:8000
    # python manage.py makemigrations core team services blog portfolio
    # python manage.py collectstatic --noinput
fi