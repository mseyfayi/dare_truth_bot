from telegram.ext import Updater, CommandHandler

from commands import start

if __name__ == '__main__':
    updater = Updater('1663301535:AAFlj2PjCoYzfTBgkHDY3bizwA0nL9Agn18')
    dp = updater.dispatcher

    handlers = [
        CommandHandler('start', start),
    ]

    for h in handlers:
        dp.add_handler(h)

    updater.start_polling()
    updater.idle()
