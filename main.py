from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from callback import callback
from commands import start

if __name__ == '__main__':
    updater = Updater('1663301535:AAFlj2PjCoYzfTBgkHDY3bizwA0nL9Agn18')
    dp = updater.dispatcher

    handlers = [
        CommandHandler('start', start),
        CallbackQueryHandler(callback)
    ]

    for h in handlers:
        dp.add_handler(h)

    updater.start_polling()
    updater.idle()
