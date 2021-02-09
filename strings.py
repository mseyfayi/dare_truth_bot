class StringsSubclass:
    def __init__(self, text: str, buttons: dict):
        super()
        self.text = text
        self.buttons = buttons


class Commands:
    def __init__(self, start: StringsSubclass):
        self.start = start


class Strings:
    def __init__(self, commands: Commands):
        self.commands = commands


strings: Strings = Strings(
    Commands(
        StringsSubclass(
            'سلام\nبه ربات جرات حقیقت خوش اومدین!\nبرای شروع روی یکی از دکمه‌های زیر بزنین:',
            {
                'help': 'راهنما',
                'play': 'بازی',
                'send_question': 'ارسال سوال'
            }
        )
    )
)
