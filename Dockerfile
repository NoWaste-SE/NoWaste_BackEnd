FROM python:3.9.0-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install gunicorn

# Install system dependencies necessary for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

# Expose the necessary port(s)
EXPOSE 8080
