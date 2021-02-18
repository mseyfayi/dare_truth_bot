from typing import Optional, List

from telegram import InlineKeyboardButton, KeyboardButton

from bot.callback_data import callbacks


def build_menu(buttons: List[InlineKeyboardButton], n_cols: int,
               header_buttons: Optional[List[InlineKeyboardButton]] = None,
               footer_buttons: Optional[List[InlineKeyboardButton]] = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def create_inline_button(
        buttons: dict,
        name: str,
        is_inline: Optional[bool] = True,
        callback_data_name: Optional[str] = None,
        switch_inline_query: Optional[str] = None,
        callback_data_creator_payload: Optional[any] = None
):
    Type = InlineKeyboardButton if is_inline else KeyboardButton
    btn = buttons[name]
    if switch_inline_query is not None:
        return Type(btn, switch_inline_query=switch_inline_query)
    else:
        callback_data = callbacks[callback_data_name] if callback_data_name else callbacks[name]
        if callback_data_creator_payload:
            return Type(btn, callback_data=callback_data(callback_data_creator_payload))
        else:
            return Type(btn, callback_data=callback_data())
