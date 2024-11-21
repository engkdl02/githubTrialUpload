
FROM python:3.10-alpine

RUN pip install pipenv
RUN mkdir -p /usr/src/app/app
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock main.py ./
COPY app ./app


CMD ls -l



