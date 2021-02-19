from decouple import config

import utils


def listen():
    handlers = [
        # CommandHandler('start', start),
    ]

    utils.listen(config('ADMIN_BOT_TOKEN'), handlers)
