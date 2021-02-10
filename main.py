from decouple import config
from telegram import User
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler

from callback import callback
from commands import start
from game import Game
from inline import inline
from user import MyUser


def load_data():
    Game.load_all()
    MyUser.load_all()


if __name__ == '__main__':
    load_data()

    updater = Updater(config('BOT_TOKEN'))
    dp = updater.dispatcher

    handlers = [
        CommandHandler('start', start),
        InlineQueryHandler(inline),
        CallbackQueryHandler(callback)
    ]

    for h in handlers:
        dp.add_handler(h)

    updater.start_polling()
    updater.idle()
