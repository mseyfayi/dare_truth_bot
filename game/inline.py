import uuid
from typing import List

from telegram import Update, InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardMarkup, \
    MessageEntity, User
from telegram.ext import CallbackContext

from strings import strings
from utils import build_menu, create_inline_button

inline_strings = strings.game.inline


def inline(update: Update, context: CallbackContext):
    user = update.inline_query.from_user
    name = user.first_name
    article = create_article(name, [name], user)
    context.bot.answer_inline_query(update.inline_query.id, [article])


def create_article(name: str, members: List[str], user: User) -> InlineQueryResultArticle:
    content = InputTextMessageContent(inline_strings.query_result.text(name, members), parse_mode=ParseMode.MARKDOWN)
    buttons = inline_strings.query_result.buttons
    button_list = [
        create_inline_button(buttons, 'start', callback_data_creator_payload=user.id),
        create_inline_button(buttons, 'get_in')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    article = InlineQueryResultArticle(str(uuid.uuid4()), inline_strings.button, content, reply_markup=reply_markup)
    return article
