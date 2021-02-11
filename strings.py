from typing import Optional, Union, Callable


class StringsTextBtn:
    def __init__(self, text: Union[str, Callable[..., str]], buttons: Optional[dict]):
        self.text = text
        self.buttons = buttons


class Commands:
    def __init__(self, start: StringsTextBtn):
        self.start = start


class Callbacks:
    def __init__(self, not_found_alert: str, edit_text: Callable[[any], str]):
        self.not_found_alert = not_found_alert
        self.edit_text = edit_text


def create_game_inline_query_text(game) -> str:
    inviter = game.inviter.name
    members = game.members
    text = "سلام\n\n" \
           "شما توسط {} به دعوت بازی جرات حقیقت شده‌اید\n\n" \
           "در صورت تمایل به بازی کردن، دکمه 'منم هستم' را بزنید\n\n" \
           "افراد حاضر در بازی:\n\n".format(inviter)
    for i, m in enumerate(members, start=1):
        text += "{}: {} \n".format(i, m.name)
    return text


class Inline:
    def __init__(self, button: str, query_result: StringsTextBtn):
        self.button = button
        self.query_result = query_result


class GameAlerts:
    def __init__(self, start_minimum: str, start_non_inviter: str, already_got_in: str, successfully_got_in: str):
        self.start_minimum = start_minimum
        self.start_non_inviter = start_non_inviter
        self.already_got_in = already_got_in
        self.successfully_got_in = successfully_got_in


class Game:
    def __init__(self, alert: GameAlerts):
        self.alert = alert


class Strings:
    def __init__(self, commands: Commands, callbacks: Callbacks, inline: Inline, game: Game):
        self.commands = commands
        self.callbacks = callbacks
        self.game = game
        self.inline = inline


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
        'ان شا اللّه بزودی آماده می‌شه :))',
        create_game_inline_query_text
    ),
    Inline(
        "ارسال",
        StringsTextBtn(
            create_game_inline_query_text,
            {
                'start': 'شروع بازی',
                'get_in': 'منم هستم'
            }
        )
    ),
    Game(
        GameAlerts(
            "باید تعداد بیشتری عضو بشن",
            "فقط دعوت‌کننده است که میتونه شروع کنه",
            "شما قبلا عضو شدی",
            "صبر کن تا دعوت‌کننده شروع کنه"
        )
    )
)
