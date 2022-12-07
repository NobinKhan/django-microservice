FROM python:3.11.0-slim-bullseye
LABEL maintainer="nazrulkhan.dk@gmail.com"

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

# setting work directory
WORKDIR /project

# copy project files
COPY ./pyproject.toml ./pyproject.toml
COPY ./manage.py ./manage.py
COPY ./settings ./settings
COPY ./account ./account
COPY ./run.sh ./run.sh

# install psycopg dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev git curl && rm -rf /var/lib/apt/lists/* && pip install --upgrade pip setuptools

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -
RUN export PATH="/root/.local/bin:$PATH"

# Install project dependency
RUN /root/.local/bin/poetry install