#!/usr/bin/python3

import os
import json

from flask import Flask, request, abort
from threading import Timer

import gemini_bot
import reply

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, PushMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)
BOT_TIMEOUT = 900

line_secret = os.environ["LINE_BOT_SECRET"]
line_userid = os.environ["LINE_BOT_USERID"]
access_token = os.environ["LINE_BOT_TOKEN"]
geminibot = {}
bot_timer = {}
bot_hint = {}
user_profile = {}
auto_reply = reply.AutoReplyManager()

configuration = Configuration(access_token=access_token)
handler = WebhookHandler(line_secret)

def chat_mode(txt) :
    bot = None

    if txt.startswith('mode:chat') :
        bot = gemini_bot.ChatBot()
    elif txt.startswith('mode:trans') :
        bot = gemini_bot.TransBot()
    elif txt.startswith('mode:teach') :
        bot = gemini_bot.TeachBot()

    return bot

def get_hash(src, stype='') :
    bothash = 'defbot'

    if src.type == 'user' or stype == 'user' :
        bothash = src.user_id[:6]
    elif src.type == 'group' or stype == 'group' :
        bothash = src.group_id[:6]

    return bothash

def split_message(txt):
    lines = txt.split('\n')
    first_line = lines[0]
    other_lines = '\n'.join(lines[1:])
    return first_line, other_lines

def update_emojis_index(emjs, idx, leng) :
    for emj in emjs :
        if emj.index > idx :
            emj.index = emj.index - leng

def show_emojis_mark(txt, emjs) :
    for emj in emjs :
        print(emj.index, txt[emj.index - 1:emj.index + 2], flush=True)

def proc_reply(msg) :
    txt = msg.text
    if msg.emojis :
        for emj in sorted(msg.emojis, key=lambda x: x.index, reverse=True) :
            #ss = txt[emj.index:emj.index + emj.length]
            txt = txt[:emj.index] + '$' + txt[emj.index + emj.length:]
            update_emojis_index(msg.emojis, emj.index, emj.length - 1)  # '$'
            delattr(emj,'length')
        #show_emojis_mark(txt, msg.emojis)

    (fl, ol) = split_message(txt)
    if msg.emojis :
        update_emojis_index(msg.emojis, 0, len(fl) + 1) # '\n'
        #show_emojis_mark(ol, msg.emojis)

    (fl, ol) = split_message(ol)
    if msg.emojis :
        update_emojis_index(msg.emojis, 0, len(fl) + 1) # '\n'
        #show_emojis_mark(ol, msg.emojis)

    return fl, ol, msg.emojis

def set_reply(msg) :
    global auto_reply
    reply = None
    txt = msg.text
    #print(proc_reply(msg), flush=True)
    (fl, ol) = split_message(txt)
    if fl.startswith('reply:add') :
        #(fl, ol) = split_message(ol)
        (fl, ol, emjs) = proc_reply(msg)
        if fl and ol :
            if auto_reply.get_message(fl) == None :
                auto_reply.add_message(fl, ol, emjs)
                reply = 'add ' + fl
            else :
                auto_reply.update_message(fl, ol, emjs)
                reply = 'update ' + fl
    elif fl.startswith('reply:del') :
        (fl, ol) = split_message(ol)
        auto_reply.delete_message(fl)
        reply = 'delete ' + fl
    else :
        lst = auto_reply.list_messages()
        reply = ''
        for it in lst :
            reply = reply + it['key'] + '  >>\n===== ' +  it['time'].strftime('%m-%d %H:%M') + ' =====\n' + it['msg'] + '\n====================\n\n'
    return reply

def proc_msg(evt) :
    global geminibot
    global bot_hint
    global auto_reply

    bothash = get_hash(evt.source)
    reply = None
    emjs = None

    txt = evt.message.text
    if txt.startswith('mode:') :
        geminibot[bothash] =  chat_mode(txt)
        bot_hint[bothash] = True

        if bothash in geminibot and geminibot[bothash] :
            reply = geminibot[bothash].greet()
        else :
            reply = 'shutdown bot'
    elif txt.startswith('reply:') :
        reply = set_reply(evt.message)
    else :
        if auto_reply.get_message(txt) != None :
            (reply, emjs) = auto_reply.get_message(txt)
        elif bothash in geminibot and geminibot[bothash] :
            reply = geminibot[bothash].send_message(txt)
        elif not bothash in bot_hint or bot_hint[bothash]:
            bot_hint[bothash] = False
            reply = 'bot 支援三模式\n可以輸入 mode:xxxx 切換模式\nmode:chat (聊天)\nmode:trans (翻譯)\nmode:teach (教學)'

    return reply, emjs

def push_message(evt, txt) :
    if evt.source.type == 'user' :
        to_id = evt.source.user_id
    else :
        to_id = evt.source.group_id

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=to_id,
                messages=[TextMessage(text=txt)]
            )
        )

def reply_message(evt, txtmsg) :
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=evt.reply_token,
                messages=[txtmsg]
            )
        )

def fetch_user_profile(src) :
    global user_profile
    uhash = get_hash(src, 'user')
    if uhash not in user_profile :
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            user_profile[uhash] = line_bot_api.get_profile(user_id=src.user_id)
            print(user_profile[uhash], flush=True)

def shutdown_bot(evt) :
    global geminibot

    bothash = get_hash(evt.source)

    if bothash in geminibot and geminibot[bothash] :
        app.logger.info("shutdown bot geminibot[" + bothash + "]")
        push_message(evt, "shutdown bot")
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

    (reply, emjs) = proc_msg(event)
    if reply :
        reply_message(event, TextMessage(text=reply, emojis=emjs))

    bothash = get_hash(event.source)
    if bothash in bot_timer and bot_timer[bothash] :
        bot_timer[bothash].cancel()
    bot_timer[bothash] = Timer(BOT_TIMEOUT, shutdown_bot, (event,))
    bot_timer[bothash].start()

    fetch_user_profile(event.source)

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)

