FROM python:3.8-slim

MAINTAINER THIDANG="dkthi2901@gmail.com"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src /app

EXPOSE 5000

CMD ["python", "server.py"]