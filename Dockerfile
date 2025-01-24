FROM python:3.10-slim

RUN apt-get update && apt-get install -y postgresql-client build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN adduser --disabled-password app-user
USER app-user

COPY src /src

WORKDIR /src
ENV PYTHONPATH="${PYTHONPATH}:/src"
EXPOSE 8000