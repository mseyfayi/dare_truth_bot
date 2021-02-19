from decouple import config
from telegram.ext import CommandHandler, CallbackQueryHandler, InlineQueryHandler

import utils
from main_bot.callback import callback
from main_bot.commands import start
from main_bot.conversation import send_question_conv
from main_bot.inline import inline


def listen():
    handlers = [
        CommandHandler('start', start),
        InlineQueryHandler(inline),
        send_question_conv,
        CallbackQueryHandler(callback)
    ]

    utils.listen(config('BOT_TOKEN'), handlers)
