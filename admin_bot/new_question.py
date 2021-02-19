from typing import Optional

from telegram import ReplyMarkup, InlineKeyboardMarkup
from telegram.ext import Dispatcher

from entities.admin import Admin
from strings import strings
from utils import create_inline_button, build_menu

new_question_strings = strings.admin.admin_new_question


def send_alert_to_admins(dispatcher: Dispatcher):
    strs = new_question_strings.new_question_added
    buttons = [create_inline_button(strs.buttons, t)
               for t in strs.buttons.keys()]
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2))

    for a in Admin.instances_list:
        _send(dispatcher, a.chat_id, strs.text, reply_markup)
    pass


def _send(dispatcher: Dispatcher, chat_id: int, text: str, reply_markup: Optional[ReplyMarkup] = None):
    dispatcher.bot.send_message(chat_id, text, reply_markup=reply_markup)
