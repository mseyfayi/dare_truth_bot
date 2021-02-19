from typing import Optional, Callable

from telegram import Update, InlineKeyboardMarkup, ReplyMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext

from callback_data import CallbackDataType
from entities.question import Question
from strings import strings
from utils import create_inline_button, build_menu

SHOW_QUESTION, = range(1)

strs = strings.admin.admin_new_question


def next_question() -> Question:
    inactive_questions = [q for q in Question.instances.values() if not q.is_active]
    yield inactive_questions


def show_question(update: Update, context: CallbackContext) -> int:
    # todo confirm or refuse or skip
    message = update.callback_query.message

    question = next_question()

    def edit_message(text: str, reply_markup: Optional[ReplyMarkup] = None):
        context.bot.edit_message_text(text, message.chat_id, message.message_id, reply_markup=reply_markup)

    if question:
        show_next_question(edit_message, question)
        return SHOW_QUESTION
    else:
        edit_message(strs.questions_finished)
        return ConversationHandler.END


def show_next_question(edit_message: Callable[[str, ReplyMarkup], None], question: Question):
    crs_question = strs.crs_question
    text = crs_question.text(question)
    buttons = [
        create_inline_button(crs_question.buttons, 'admin_confirm', callback_data_creator_payload=question.id),
        create_inline_button(crs_question.buttons, 'admin_refuse', callback_data_creator_payload=question.id),
    ]
    footer = [create_inline_button(crs_question.buttons, 'admin_skip')]
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2, footer_buttons=footer))
    edit_message(text, reply_markup)


confirm_question_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(show_question,
                                       pattern='^{}$'.format(CallbackDataType.ADMIN_SHOW_QUESTIONS.value))],
    states={
        SHOW_QUESTION: [CallbackQueryHandler(show_question,
                                             pattern='^({}|{}|{})$'.format(
                                                 CallbackDataType.ADMIN_SHOW_QUESTIONS.value,
                                                 CallbackDataType.ADMIN_SHOW_QUESTIONS.value,
                                                 CallbackDataType.ADMIN_SHOW_QUESTIONS.value,
                                             ))]
    },
    fallbacks=[],
)
