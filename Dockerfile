FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt requirements-airflow.txt ./

RUN pip install -r requirements.txt \
    && pip install -r requirements-airflow.txt

COPY . .

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser
