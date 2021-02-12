from typing import Optional, Union, Callable


class StringsTextBtn:
    def __init__(self, text: Union[str, Callable[..., str]], buttons: Optional[dict]):
        self.text = text
        self.buttons = buttons


class Commands:
    def __init__(self, start: StringsTextBtn):
        self.start = start


class Callbacks:
    def __init__(self, bot_link_btn: str, not_found_alert: str, edit_text1: Callable[[any], str],
                 edit_text2: StringsTextBtn,
                 edit_text3: StringsTextBtn):
        self.bot_link_btn = bot_link_btn
        self.not_found_alert = not_found_alert
        self.edit_text1 = edit_text1
        self.edit_text2 = edit_text2
        self.edit_text3 = edit_text3


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


def create_game_choose_text(game) -> str:
    user = game.turn.name
    text = "نوبت {}:\n\n" \
           "یکی رو انتخاب کن:\n\n".format(user)
    return text


dtc = {
    'dare': 'جرات',
    'truth': 'حقیقت',
}


def create_game_answer_text(user: str, dtc_type: str, question: str) -> str:
    dtc_text = dtc[dtc_type]
    text = "کاربر '{}' {} رو انتخاب کرد\n\n" \
           "متن سوال:\n\n" \
           "{}\n\n" \
           "بعد جواب دادن دکمه جواب دادم رو بزن\n\n".format(user, dtc_text, question)
    return text


class Inline:
    def __init__(self, button: str, query_result: StringsTextBtn):
        self.button = button
        self.query_result = query_result


class GameAlerts:
    def __init__(self, start_minimum: str, start_non_inviter: str, already_got_in: str, successfully_got_in: str,
                 not_ur_turn: str):
        self.start_minimum = start_minimum
        self.start_non_inviter = start_non_inviter
        self.already_got_in = already_got_in
        self.successfully_got_in = successfully_got_in
        self.not_ur_turn = not_ur_turn


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
        'بات جرات-حقیقت',
        'ان شا اللّه بزودی آماده می‌شه :))',
        create_game_inline_query_text,
        StringsTextBtn(
            create_game_choose_text,
            dtc
        ),
        StringsTextBtn(
            create_game_answer_text,
            {
                'answered': 'جواب دادم',
            }
        )
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
            "صبر کن تا دعوت‌کننده شروع کنه",
            "اکنون نوبت شما نیست"
        )
    )
)
