from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from strings import strings
from utils import build_menu, create_inline_button

command_strings = strings.commands

start_button_list = [
    create_inline_button(command_strings.start.buttons, "help"),
    create_inline_button(command_strings.start.buttons, "play", switch_inline_query=""),
    create_inline_button(command_strings.start.buttons, "send_question"),
]

start_reply_markup = InlineKeyboardMarkup(build_menu(start_button_list, n_cols=2))


def start(update: Update, context: CallbackContext):
    start_strings = command_strings.start
    context.bot.send_message(update.message.chat_id, text=start_strings.text, reply_markup=start_reply_markup)
