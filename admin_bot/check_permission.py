from typing import Callable

from telegram import Message
from telegram.ext import CallbackContext

from entities.admin import Admin
from strings import strings

admin_strings = strings.admin


def check_permission(chat_id: int, context: CallbackContext,message: Message):
    def send_message(text: str):
        context.bot.send_message(message.chat_id, text)

    result = any([a for a in Admin.instances_list if a.chat_id == chat_id])

    if not result:
        send_message(admin_strings.not_allowed)
    return result
