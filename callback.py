import json
from enum import Enum
from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext
from strings import strings

callback_strings = strings.callbacks


class CallbackDataType(Enum):
    START = "START"
    GET_IN = "GET_IN"
    HELP = "NOT_FOUND"
    SEND_QUESTION = "NOT_FOUND"


class CallbackData:
    type: CallbackDataType
    payload: any


def _create_callback_data(data_type: CallbackDataType, payload: Optional = None) -> str:
    data = {'type': data_type.value}
    if payload is not None:
        data.payload = payload
    return json.dumps(data)


def help_cbd() -> str:
    return _create_callback_data(CallbackDataType.HELP)


def send_question_cbd() -> str:
    return _create_callback_data(CallbackDataType.SEND_QUESTION)


def start_cbd(starter_id: str) -> str:
    return _create_callback_data(CallbackDataType.START, starter_id)


def get_in_cbd() -> str:
    return _create_callback_data(CallbackDataType.GET_IN)


callbacks = {
    'help': help_cbd,
    'send_question': send_question_cbd,
    'start': start_cbd,
    'get_in': get_in_cbd,
}


def callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data: CallbackDataType = json.loads(query.data)
    print(data)
    data_type = data['type']

    not_found_alert = callback_strings.not_found_alert
    if data_type == CallbackDataType.HELP:
        context.bot.answer_callback_query(callback_query_id=query.id, text=not_found_alert, show_alert=True)
    elif data_type == CallbackDataType.SEND_QUESTION:
        context.bot.answer_callback_query(callback_query_id=query.id, text=not_found_alert, show_alert=True)
    elif data_type == CallbackDataType.GET_IN:
        context.bot.answer_callback_query(callback_query_id=query.id, text=not_found_alert, show_alert=True)
    elif data_type == CallbackDataType.START:
        context.bot.answer_callback_query(callback_query_id=query.id, text=not_found_alert, show_alert=True)
    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text=not_found_alert, show_alert=True)
