from decouple import config

import utils
from admin_bot.start import start_conv


def listen():
    handlers = [
        start_conv,
    ]

    utils.listen(config('ADMIN_BOT_TOKEN'), handlers)
