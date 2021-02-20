from enum import Enum
from typing import Optional, Tuple, Union, List


class CallbackDataType(Enum):
    START = "START"
    GET_IN = "GET_IN"
    HELP = "NOT_FOUND"
    SEND_QUESTION = "SEND_QUESTION"
    SEND_QUESTION_TYPE = "SEND_QUESTION_TYPE"
    SEND_QUESTION_CANCEL = "SEND_QUESTION_CANCEL"
    CHOOSE = "CHOOSE"
    ANSWER = "ANSWER"
    VOTE = "VOTE"

    ADMIN_SHOW_QUESTIONS = "ADMIN_SHOW_QUESTIONS"
    ADMIN_REFUSE_QUESTIONS = "ADMIN_REFUSE_QUESTIONS"
    ADMIN_CONFIRM_QUESTIONS = "ADMIN_CONFIRM_QUESTIONS"
    ADMIN_END_QUESTIONS = "ADMIN_END_QUESTIONS"

    ADMIN_ADD_QUESTION_TYPE = "ADMIN_ADD_QUESTION_TYPE"
    ADMIN_ADD_QUESTION_CANCEL = "ADMIN_ADD_QUESTION_CANCEL"


def _create_callback_data(data_type: CallbackDataType, payload: Optional = None) -> str:
    data = data_type.value
    if payload is not None:
        data += ";" + payload
    return data


def restore_callback_data(data: str) -> Tuple[str, Union[List, None]]:
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


def send_question_type_cbd(payload: str) -> str:
    return _create_callback_data(CallbackDataType.SEND_QUESTION_TYPE, payload)


def send_question_cancel_cdn() -> str:
    return _create_callback_data(CallbackDataType.SEND_QUESTION_CANCEL)


def start_cbd(start_payload: str) -> str:
    return _create_callback_data(CallbackDataType.START, start_payload)


def get_in_cbd(get_in_payload: str) -> str:
    return _create_callback_data(CallbackDataType.GET_IN, get_in_payload)


def dare_cbd(payload: str = None):
    return _create_callback_data(CallbackDataType.CHOOSE, payload)


def truth_cbd(payload: str = None):
    return _create_callback_data(CallbackDataType.CHOOSE, payload)


def answer_cbd(payload: str):
    return _create_callback_data(CallbackDataType.ANSWER, payload)


def vote_cbd(payload: str):
    return _create_callback_data(CallbackDataType.VOTE, payload)


def admin_show_questions_cbd():
    return _create_callback_data(CallbackDataType.ADMIN_SHOW_QUESTIONS)


def admin_confirm_questions_cbd(payload: str):
    return _create_callback_data(CallbackDataType.ADMIN_CONFIRM_QUESTIONS, payload)


def admin_refuse_questions_cbd(payload: str):
    return _create_callback_data(CallbackDataType.ADMIN_REFUSE_QUESTIONS, payload)


def admin_end_questions_cbd():
    return _create_callback_data(CallbackDataType.ADMIN_END_QUESTIONS)


def admin_add_question_type_cbd(payload: str) -> str:
    return _create_callback_data(CallbackDataType.ADMIN_ADD_QUESTION_TYPE, payload)


def admin_add_question_cancel_cdn() -> str:
    return _create_callback_data(CallbackDataType.ADMIN_ADD_QUESTION_CANCEL)


callbacks = {
    'help': help_cbd,
    'send_question': send_question_cbd,
    'send_question_type': send_question_type_cbd,
    'send_question_cancel': send_question_cancel_cdn,
    'start': start_cbd,
    'get_in': get_in_cbd,
    'dare': dare_cbd,
    'truth': truth_cbd,
    'answered': answer_cbd,
    'yes': vote_cbd,
    'no': vote_cbd,

    'admin_show': admin_show_questions_cbd,
    'admin_refuse': admin_refuse_questions_cbd,
    'admin_confirm': admin_confirm_questions_cbd,
    'admin_end': admin_end_questions_cbd,

    'admin_add_question_type': admin_add_question_type_cbd,
    'admin_add_question_cancel': admin_add_question_cancel_cdn,
}
