import json
from enum import Enum
from typing import Optional, Dict, List

from telegram import Update
from telegram.ext import CallbackContext

from game import start
from strings import strings

callback_strings = strings.callbacks


class CallbackDataType(Enum):
    START = "START"
    GET_IN = "GET_IN"
    HELP = "NOT_FOUND"
    SEND_QUESTION = "NOT_FOUND"


def _create_callback_data(data_type: CallbackDataType, payload: Optional = None) -> str:
    data = {'type': data_type.value}
    if payload is not None:
        data['payload'] = payload
    return json.dumps(data)


def help_cbd() -> str:
    return _create_callback_data(CallbackDataType.HELP)


def send_question_cbd() -> str:
    return _create_callback_data(CallbackDataType.SEND_QUESTION)


def start_cbd(start_payload: Dict[str, str]) -> str:
    return _create_callback_data(CallbackDataType.START, start_payload)


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
    data = json.loads(query.data)
    not_found_alert = callback_strings.not_found_alert

    def alert(text: str):
        context.bot.answer_callback_query(callback_query_id=query.id, text=text, show_alert=True)

    print(data)
    data_type = data['type']
    if data_type == CallbackDataType.HELP.value:
        alert(not_found_alert)
    elif data_type == CallbackDataType.SEND_QUESTION.value:
        alert(not_found_alert)
    elif data_type == CallbackDataType.GET_IN.value:
        alert(not_found_alert)
    elif data_type == CallbackDataType.START.value:
        payload: str = data['payload']
        [starter_id, game_id] = payload.split(';')
        start(starter_id, game_id, alert)
    else:
        print("koft1")
