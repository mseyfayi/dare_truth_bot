import uuid

from telegram import Update, InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from game import Game
from strings import strings
from user import MyUser
from utils import build_menu, create_inline_button

inline_strings = strings.inline


def inline(update: Update, context: CallbackContext):
    user = update.inline_query.from_user
    game = Game(MyUser.new(user.id, user.first_name))
    article = create_article(game)
    context.bot.answer_inline_query(update.inline_query.id, [article])


def create_inline_markup(game: Game):
    game_id = game.game_id
    buttons = inline_strings.query_result.buttons
    start_payload = "{}".format(game_id)
    get_in_payload = "{}".format(game_id)
    button_list = [
        create_inline_button(buttons, 'start', callback_data_creator_payload=start_payload),
        create_inline_button(buttons, 'get_in', callback_data_creator_payload=get_in_payload)
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup


def create_article(game: Game) -> InlineQueryResultArticle:
    content = InputTextMessageContent(inline_strings.query_result.text(game), parse_mode=ParseMode.MARKDOWN)
    reply_markup = create_inline_markup(game)
    article = InlineQueryResultArticle(str(uuid.uuid4()), inline_strings.button, content, reply_markup=reply_markup)
    return article
