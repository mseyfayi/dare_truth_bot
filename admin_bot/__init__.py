import threading
from typing import Optional

from decouple import config
from telegram.ext import Dispatcher

import utils
from admin_bot.add_question_cnv import add_question_conv
from admin_bot.confirm_question_conv import confirm_question_conv
from admin_bot.new_question_alert import send_alert_to_admins
from admin_bot.start import start_conv

dispatcher: Optional[Dispatcher] = None


def bot_listen():
    handlers = [
        start_conv,
        confirm_question_conv,
        add_question_conv
        # todo change question
    ]

    global dispatcher
    dispatcher = utils.listen(config('ADMIN_BOT_TOKEN'), handlers)


event = threading.Event()


def call_new_question_event():
    event.set()


def _event_listener():
    while True:
        global event
        event.wait()
        send_alert_to_admins(dispatcher)
        event = threading.Event()


def question_listen():
    thread = threading.Thread(target=_event_listener, name='_event_listener')
    thread.start()
