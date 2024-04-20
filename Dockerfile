FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY ./requirements.txt ./

RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

RUN chmod -R 777 ./