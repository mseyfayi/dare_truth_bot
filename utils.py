from typing import Optional, List, Union

from telegram import InlineKeyboardButton

from bot.callback_data import callbacks


def build_menu(buttons: List[Union[InlineKeyboardButton]], n_cols: int,
               header_buttons: Optional[List[Union[InlineKeyboardButton]]] = None,
               footer_buttons: Optional[List[Union[InlineKeyboardButton]]] = None) \
        -> List[List[Union[InlineKeyboardButton]]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def create_inline_button(
        buttons: dict,
        name: str,
        callback_data_name: Optional[str] = None,
        switch_inline_query: Optional[str] = None,
        callback_data_creator_payload: Optional[any] = None
) -> Union[InlineKeyboardButton]:
    btn = buttons[name]
    if switch_inline_query is not None:
        return InlineKeyboardButton(btn, switch_inline_query=switch_inline_query)
    else:
        callback_data = callbacks[callback_data_name] if callback_data_name else callbacks[name]
        if callback_data_creator_payload:
            return InlineKeyboardButton(btn, callback_data=callback_data(callback_data_creator_payload))
        else:
            return InlineKeyboardButton(btn, callback_data=callback_data())
