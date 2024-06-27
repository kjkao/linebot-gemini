#!/bin/bash

DI=python3-services
DN=python3-linebot-gemini

docker stop $DN
docker rm $DN

ENVS="-e LINE_BOT_SECRET=$LINE_BOT_SECRET -e GEMINI_API_KEY=$GEMINI_API_KEY -e LINE_BOT_TOKEN=$LINE_BOT_TOKEN -e LINE_BOT_USERID=$LINE_BOT_USERID"
VOLS="-v $HOME/github/linebot-gemini/line-bot:/home/user1000/line-bot"
CMD="/home/user1000/line-bot/run-line-bot.sh"
ARGS="-d -i --restart unless-stopped --network host"
docker run $ARGS --name $DN $VOLS $PORTS $ENVS $DI $CMD
