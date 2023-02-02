poetry run gunicorn settings.asgi:application -k uvicorn.workers.UvicornWorker
# poetry run uvicorn settings.asgi:application --host 0.0.0.0 --port 8080