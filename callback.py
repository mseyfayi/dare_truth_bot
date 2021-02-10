import uuid
from enum import Enum
from typing import Optional, List, Tuple, Union

from telegram import Update
from telegram.ext import CallbackContext

from game import Game
from strings import strings

callback_strings = strings.callbacks


class CallbackDataType(Enum):
    START = "START"
    GET_IN = "GET_IN"
    HELP = "NOT_FOUND"
    SEND_QUESTION = "NOT_FOUND"


def _create_callback_data(data_type: CallbackDataType, payload: Optional = None) -> str:
    data = data_type.value
    if payload is not None:
        data += ";" + payload
    return data


def _restore_callback_data(data: str) -> Tuple[str, Union[List, None]]:
    if data.find(";"):
        split: List[str] = data.split(";")
        type, payloads = split[0], split[1:]
        return type, payloads
    else:
        return data, None


def help_cbd() -> str:
    return _create_callback_data(CallbackDataType.HELP)


def send_question_cbd() -> str:
    return _create_callback_data(CallbackDataType.SEND_QUESTION)


def start_cbd(start_payload: str) -> str:
    return _create_callback_data(CallbackDataType.START, start_payload)


def get_in_cbd(get_in_payload: str) -> str:
    return _create_callback_data(CallbackDataType.GET_IN, get_in_payload)


callbacks = {
    'help': help_cbd,
    'send_question': send_question_cbd,
    'start': start_cbd,
    'get_in': get_in_cbd,
}


def callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data
    not_found_alert = callback_strings.not_found_alert

    def alert(text: str):
        context.bot.answer_callback_query(callback_query_id=query.id, text=text, show_alert=True)

    print("received: ", data)
    data_type, payloads = _restore_callback_data(data)
    if CallbackDataType.HELP.value == data_type:
        alert(not_found_alert)
    elif CallbackDataType.SEND_QUESTION.value == data_type:
        alert(not_found_alert)
    elif CallbackDataType.GET_IN.value == data_type:
        [game_id] = payloads
        game = Game.get_instance(game_id)
        user_id = user.id
        game.get_in(user_id,alert)
    elif CallbackDataType.START.value == data_type:
        [game_id] = payloads
        starter_id = user.id
        game = Game.get_instance(game_id)
        game.start(starter_id, alert)
    else:
        print("koft1")
