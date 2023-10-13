FROM python:3.11.4-slim-buster
RUN apt update && apt upgrade -y
RUN apt-get -y install git
RUN apt-get install -y wget python3-pip curl bash neofetch ffmpeg software-properties-common
COPY requirements.txt .
RUN apt-get install -y nodejs
COPY . .
RUN pip install -U "pip < 22" setuptools wheel && pip install -U -r requirements.txt
RUN python3 -m MissCutie
