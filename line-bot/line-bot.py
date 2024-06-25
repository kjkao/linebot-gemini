#!/usr/bin/python3

from flask import Flask, request, abort

import os
import json

import gemini_chat
import gemini_trans
import gemini_teach

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

CHAT_MODE = 0
app = Flask(__name__)

line_secret = os.environ["LINE_BOT_SECRET"]
access_token = os.environ["LINE_BOT_TOKEN"]
geminibot = None

configuration = Configuration(access_token=access_token)
handler = WebhookHandler(line_secret)

def chat_mode(msg) :
    mode = 0

    if msg.startswith('mode:chat') :
        mode = 1
    elif msg.startswith('mode:trans') :
        mode = 2
    elif msg.startswith('mode:teach') :
        mode = 3
    else :
        mode = 0

    return mode

def proc_msg(msg) :
    global CHAT_MODE
    global geminibot

    if msg.startswith('mode:') :

        CHAT_MODE = chat_mode(msg)

        geminibot = None
        if CHAT_MODE == 1 :
            reply = "change mode to Chat"
            geminibot = gemini_chat.ChatBot()
        elif CHAT_MODE == 2 :
            reply = "change mode to Translate"
            geminibot = gemini_trans.TransBot()
        elif CHAT_MODE == 3 :
            reply = "change mode to English Teacher"
            geminibot = gemini_teach.TeachBot()
        else :
            reply = msg
    else :
        if CHAT_MODE == 1 :
            resp = geminibot.send_message(msg)
            reply = "mode:chat\n" + resp
        elif CHAT_MODE == 2 :
            resp = geminibot.send_message(msg)
            reply = "mode:translate\n" + resp
        elif CHAT_MODE == 3 :
            resp = geminibot.send_message(msg)
            reply = "mode:teach\n" + resp
        else :
            reply = msg
    #print(msg, flush=True)
    #print(reply, flush=True)
    return reply

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
    with ApiClient(configuration) as api_client:
        reply = proc_msg(event.message.text)
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)]
            )
        )

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)

