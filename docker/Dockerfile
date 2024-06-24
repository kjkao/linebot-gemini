FROM python:3.11

ARG UID=1000
ARG UNAME=user$UID
ARG GID=$UID

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN apt-get update
RUN apt-get -y install vim cron net-tools
RUN pip install line-bot-sdk flask google-generativeai

EXPOSE 8080
USER $UNAME
WORKDIR /home/$UNAME
