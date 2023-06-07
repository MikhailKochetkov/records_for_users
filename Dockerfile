FROM python:3.10-slim

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . /api

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get install -y ffmpeg

ENV HOST="127.0.0.1"

ENV PORT=8000

ENV DB_NAME="database.db"

ENV DATABASE_URL="sqlite:///"

CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8000"]