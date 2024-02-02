FROM ubuntu:python:3.11
LABEL authors="AMDisPOWER"

RUN mkdir /literature

WORKDIR /literature

COPY pyproject.toml .

RUN pip install poetry
RUN poetry install
RUN poetry add gunicorn

COPY . .

ENTRYPOINT ["top", "-b"]