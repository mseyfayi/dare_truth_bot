from typing import Optional


class StringsTextBtn:
    def __init__(self, text: str, buttons: Optional[dict]):
        self.text = text
        self.buttons = buttons


class Commands:
    def __init__(self, start: StringsTextBtn):
        self.start = start


class Callbacks:
    def __init__(self, not_found_alert: str):
        self.not_found_alert = not_found_alert


class Strings:
    def __init__(self, commands: Commands, callbacks: Callbacks):
        self.commands = commands
        self.callbacks = callbacks


strings: Strings = Strings(
    Commands(
        StringsTextBtn(
            'سلام\nبه ربات جرات حقیقت خوش اومدین!\nبرای شروع روی یکی از دکمه‌های زیر بزنین:',
            {
                'help': 'راهنما',
                'play': 'بازی',
                'send_question': 'ارسال سوال'
            }
        )
    ),
    Callbacks(
        'ان شا اللّه بزودی آماده می‌شه :))'
    )
)
