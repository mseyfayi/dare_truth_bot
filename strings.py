from typing import Optional, Union, Callable, List


class StringsTextBtn:
    def __init__(self, text: Union[str, Callable[..., str]], buttons: Optional[dict]):
        self.text = text
        self.buttons = buttons


class Commands:
    def __init__(self, start: StringsTextBtn):
        self.start = start


class Callbacks:
    def __init__(self, not_found_alert: str):
        self.not_found_alert = not_found_alert


def create_game_inline_query_text(inviter: str, members: List[str]):
    text = "سلام\n\n" \
           "شما توسط {} به دعوت بازی جرات حقیقت شده‌اید\n\n" \
           "در صورت تمایل به بازی کردن، دکمه 'منم هستم' را بزنید\n\n" \
           "افراد حاضر در بازی:\n\n".format(inviter)
    for i, m in enumerate(members, start=1):
        text += "{}: {} \n".format(i, m)
    return text


class Inline:
    def __init__(self, button: str, query_result: StringsTextBtn):
        self.button = button
        self.query_result = query_result


class Game:
    def __init__(self, inline: Inline):
        self.inline = inline


class Strings:
    def __init__(self, commands: Commands, callbacks: Callbacks, game: Game):
        self.commands = commands
        self.callbacks = callbacks
        self.game = game


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
    ),
    Game(
        Inline(
            "ارسال",
            StringsTextBtn(
                create_game_inline_query_text,
                {
                    'start': 'شروع بازی',
                    'get_in': 'منم هستم'
                }
            )
        )
    )
)
