import json
from enum import Enum
from typing import Optional


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
