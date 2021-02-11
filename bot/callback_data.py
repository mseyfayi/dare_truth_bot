from enum import Enum
from typing import Optional, Tuple, Union, List


class CallbackDataType(Enum):
    START = "START"
    GET_IN = "GET_IN"
    HELP = "NOT_FOUND"
    SEND_QUESTION = "NOT_FOUND"
    DARE = "DARE"
    TRUTH = "TRUTH"
    CHAT = "CHAT"


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


def dare_cbd(payload: str):
    return _create_callback_data(CallbackDataType.DARE, payload)


def truth_cbd(payload: str):
    return _create_callback_data(CallbackDataType.TRUTH, payload)


def chat_cbd(payload: str):
    return _create_callback_data(CallbackDataType.CHAT, payload)


callbacks = {
    'help': help_cbd,
    'send_question': send_question_cbd,
    'start': start_cbd,
    'get_in': get_in_cbd,
    'dare': dare_cbd,
    'chat': chat_cbd,
    'truth': truth_cbd,
}
