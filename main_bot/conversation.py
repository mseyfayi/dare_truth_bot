import warnings
from typing import List

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

from callback_data import CallbackDataType, restore_callback_data
from main_bot.commands import start_reply_markup
from entities.question import Question
from strings import strings
from utils import build_menu, create_inline_button

warnings.filterwarnings("ignore", message="If 'per_message=False', 'CallbackQueryHandler' will not be ")

TYPE, TEXT = range(2)

conv_strings = strings.conversations

question_type = ''


def create_cancel_btn() -> InlineKeyboardButton:
    name = 'send_question_cancel'
    buttons = {name: conv_strings.cancel_btn_text}
    return create_inline_button(buttons, name)


def create_sq_rm(button_list: List[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2, footer_buttons=[create_cancel_btn()]))


def send_question(update: Update, context: CallbackContext) -> int:
    send_string = conv_strings.send_question_type
    button_list = [create_inline_button(send_string.buttons, t,
                                        callback_data_name='send_question_type',
                                        callback_data_creator_payload=t.upper())
                   for t in send_string.buttons.keys()]

    message = update.callback_query.message
    context.bot.editMessageText(send_string.text,
                                reply_markup=create_sq_rm(button_list),
                                message_id=message.message_id,
                                chat_id=message.chat_id)

    return TYPE


def choose_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    data = query.data
    ignore, [q_type] = restore_callback_data(data)
    global question_type
    question_type = str(q_type).lower()
    context.bot.editMessageText(conv_strings.enter_question_text,
                                reply_markup=create_sq_rm([]),
                                message_id=query.message.message_id,
                                chat_id=query.message.chat_id)

    return TEXT


def writhe_text(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    # todo send to admin
    print(update.message.chat_id)
    Question(text, question_type)
    context.bot.send_message(update.message.chat_id,
                             conv_strings.send_question_success,
                             reply_markup=start_reply_markup)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    global question_type
    question_type = ''
    message = update.callback_query.message
    context.bot.editMessageText(conv_strings.send_question_cancel,
                                chat_id=message.chat_id,
                                message_id=message.message_id,
                                reply_markup=start_reply_markup)

    return ConversationHandler.END


send_question_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(send_question,
                                       pattern='^{}$'.format(CallbackDataType.SEND_QUESTION.value))],
    states={
        TYPE: [CallbackQueryHandler(choose_type,
                                    pattern='^{};(DARE|TRUTH)$'.format(CallbackDataType.SEND_QUESTION_TYPE.value))],
        TEXT: [MessageHandler(Filters.text, writhe_text)]
    },
    fallbacks=[CallbackQueryHandler(cancel,
                                    pattern='^{}$'.format(CallbackDataType.SEND_QUESTION_CANCEL.value))],
)
