import threading
from typing import Optional

from decouple import config
from telegram import Update
from telegram.ext import TypeHandler, CallbackContext, MessageHandler, Filters, Dispatcher

import utils
from admin_bot.new_question import send_alert_to_admins
from admin_bot.start import start_conv

dispatcher: Optional[Dispatcher] = None


def bot_listen():
    handlers = [
        start_conv,
    ]

    global dispatcher
    dispatcher = utils.listen(config('ADMIN_BOT_TOKEN'), handlers)


event = threading.Event()


def _send(chat_id: int, text: str):
    dispatcher.bot.send_message(chat_id, text)


def call_event():
    event.set()


def _event_listener():
    while True:
        event.wait()
        send_alert_to_admins()


def question_listen():
    thread = threading.Thread(target=_event_listener, name='_event_listener')
    thread.start()
