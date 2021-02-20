import warnings
from typing import Optional, Callable, Dict

from telegram import Update, InlineKeyboardMarkup, ReplyMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, CommandHandler

from callback_data import CallbackDataType, restore_callback_data
from entities.question import Question
from strings import strings
from utils import create_inline_button, build_menu

warnings.filterwarnings("ignore", message="If 'per_message=False', 'CallbackQueryHandler' will not be ")

SHOW_QUESTION, = range(1)

strs = strings.admin.admin_new_question


def next_question() -> Question:
    inactive_questions = [q for q in Question.instances.values() if not q.is_active]
    for q in inactive_questions:
        yield q


def show_question(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    message = query.message if query else update.message

    def edit_message(text: str, reply_markup: Optional[ReplyMarkup] = None):
        context.bot.edit_message_text(text, message.chat_id, message.message_id, reply_markup=reply_markup)

    def send_message(text: str, reply_markup: Optional[ReplyMarkup] = None):
        context.bot.send_message(message.chat_id, text, reply_markup=reply_markup)

    def delete_message():
        context.bot.delete_message(message.chat_id, message.message_id)

    if query:
        print('confirm q receive: ', query.data)
        data_type, payloads = restore_callback_data(query.data)
        if data_type == CallbackDataType.ADMIN_CONFIRM_QUESTIONS.value:
            instance = Question.get_instance(payloads[0])
            instance.confirm()
            edit_message(strs.confirmed_question(instance))
        elif data_type == CallbackDataType.ADMIN_REFUSE_QUESTIONS.value:
            Question.get_instance(payloads[0]).refuse()
            delete_message()
        else:
            delete_message()

    question = next(next_question(), None)
    if question:
        show_next_question(send_message, question)
        return SHOW_QUESTION
    else:
        send_message(strs.questions_finished)
        return ConversationHandler.END


def show_next_question(send_message: Callable[[str, ReplyMarkup], None], question: Question):
    crs_question = strs.crs_question
    text = crs_question.text(question)
    buttons = [
        create_inline_button(crs_question.buttons, 'admin_refuse', callback_data_creator_payload=question.id),
        create_inline_button(crs_question.buttons, 'admin_confirm', callback_data_creator_payload=question.id),
    ]
    footer = [create_inline_button(crs_question.buttons, 'admin_skip')]
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2, footer_buttons=footer))
    send_message(text, reply_markup)


def end_question(update: Update, context: CallbackContext) -> int:
    message = update.callback_query.message
    context.bot.edit_message_text(strs.operation_end, message.chat_id, message.message_id)
    return ConversationHandler.END


confirm_question_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(show_question, pattern='^{}$'.format(CallbackDataType.ADMIN_SHOW_QUESTIONS.value)),
        CommandHandler('show', show_question)
    ],
    states={
        SHOW_QUESTION: [CallbackQueryHandler(show_question,
                                             pattern='^({}|{}|{});.*$'.format(
                                                 CallbackDataType.ADMIN_CHANGE_QUESTIONS.value,
                                                 CallbackDataType.ADMIN_CONFIRM_QUESTIONS.value,
                                                 CallbackDataType.ADMIN_REFUSE_QUESTIONS.value,
                                             ))]
    },
    fallbacks=[
        CallbackQueryHandler(end_question, pattern='^{}$'.format(CallbackDataType.ADMIN_END_QUESTIONS.value))
    ],
)
