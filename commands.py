from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from strings import strings
from utils import build_menu, create_inline_button

command_strings = strings.commands


def start(update: Update, context: CallbackContext):
    start_strings = command_strings.start
    buttons = start_strings.buttons
    button_list = [
        create_inline_button(buttons, "help"),
        create_inline_button(buttons, "play", switch_inline_query=""),
        create_inline_button(buttons, "send_question"),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(update.message.chat_id, text=start_strings.text, reply_markup=reply_markup)
