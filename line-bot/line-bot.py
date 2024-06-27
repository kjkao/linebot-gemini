#!/usr/bin/python3

import os
import json

from flask import Flask, request, abort
from threading import Timer

import gemini_bot

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, PushMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

line_secret = os.environ["LINE_BOT_SECRET"]
line_userid = os.environ["LINE_BOT_USERID"]
access_token = os.environ["LINE_BOT_TOKEN"]
geminibot = {}
bot_timer = {}

configuration = Configuration(access_token=access_token)
handler = WebhookHandler(line_secret)

def chat_mode(msg) :
    bot = None

    if msg.startswith('mode:chat') :
        bot = gemini_bot.ChatBot()
    elif msg.startswith('mode:trans') :
        bot = gemini_bot.TransBot()
    elif msg.startswith('mode:teach') :
        bot = gemini_bot.TeachBot()

    return bot

def get_hash(evt) :
    bothash = 'defbot'

    if evt.source.type == 'user' :
        bothash = evt.source.user_id[:6]
    elif evt.source.type == 'group' :
        bothash = evt.source.group_id[:6]

    return bothash

def proc_msg(evt) :
    global geminibot

    bothash = get_hash(evt)

    msg = evt.message.text
    if msg.startswith('mode:') :

        geminibot[bothash] =  chat_mode(msg)

        if bothash in geminibot and geminibot[bothash] :
            reply = geminibot[bothash].greet()
        else :
            reply = msg
    else :
        if bothash in geminibot and geminibot[bothash] :
            reply = geminibot[bothash].send_message(msg)
        else :
            reply = msg

    return reply

def push_message(msg) :
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.push_message(
            PushMessageRequest(
                to=line_userid,
                messages=[TextMessage(text=msg)]
            )
        )


def shutdown_bot(evt) :
    global geminibot

    bothash = get_hash(evt)

    if bothash in geminibot and geminibot[bothash] :
        app.logger.info("shutdown bot geminibot[" + bothash + "]")
        #push_message("shutdown bot")
        del(geminibot[bothash])
        geminibot[bothash] = None

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    global bot_timer
    with ApiClient(configuration) as api_client:

        reply = proc_msg(event)
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)]
            )
        )

        bothash = get_hash(event)
        if bothash in bot_timer and bot_timer[bothash] :
            bot_timer[bothash].cancel()
        bot_timer[bothash] = Timer(300, shutdown_bot, (event,))
        bot_timer[bothash].start()

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)

