from typing import Optional, List

from telegram import InlineKeyboardButton

from callback import callbacks


def build_menu(buttons: List[str], n_cols: int, header_buttons: Optional[List[str]] = None,
               footer_buttons: Optional[List[str]] = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def create_inline_button(
        buttons: dict,
        name: str,
        switch_inline_query: Optional[str] = None,
        callback_data_creator_payload: Optional[any] = None
):
    btn = buttons[name]
    if switch_inline_query is not None:
        return InlineKeyboardButton(btn, switch_inline_query=switch_inline_query)
    else:
        callback_data = callbacks[name]
        if callback_data_creator_payload:
            print("callback_data:", callback_data(callback_data_creator_payload))
            print("callback_data length:", len(callback_data(callback_data_creator_payload).encode('utf-8')))
            return InlineKeyboardButton(btn, callback_data=callback_data(callback_data_creator_payload))
        else:
            return InlineKeyboardButton(btn, callback_data=callback_data())
