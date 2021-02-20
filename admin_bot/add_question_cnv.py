import warnings
from typing import List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler, CallbackContext, MessageHandler, \
    Filters

from admin_bot.check_permission import check_permission
from callback_data import CallbackDataType, restore_callback_data
from entities.question import Question
from strings import strings
from utils import create_inline_button, build_menu

warnings.filterwarnings("ignore", message="If 'per_message=False', 'CallbackQueryHandler' will not be ")

strs = strings.admin.add_question

TYPE, TEXT = range(2)

question_type = ''


def create_cancel_btn() -> InlineKeyboardButton:
    name = 'admin_add_question_cancel'
    buttons = {name: strs.cancel_btn_text}
    return create_inline_button(buttons, name)


def create_aq_rm(button_list: List[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2, footer_buttons=[create_cancel_btn()]))


def start(update: Update, context: CallbackContext) -> int:
    message = update.message

    if not check_permission(message.chat_id, context, message):
        return ConversationHandler.END

    send_string = strs.question_type
    button_list = [
        create_inline_button(send_string.buttons, t,
                             callback_data_name='admin_add_question_type',
                             callback_data_creator_payload=t.upper())
        for t in send_string.buttons.keys()
    ]

    context.bot.send_message(message.chat_id, send_string.text, reply_markup=create_aq_rm(button_list))
    return TYPE


def choose_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    data = query.data
    message = query.message
    ignore, [q_type] = restore_callback_data(data)
    global question_type
    question_type = str(q_type).lower()
    context.bot.editMessageText(strs.enter_question_text,
                                message.chat_id,
                                message.message_id,
                                reply_markup=create_aq_rm([]))
    return TEXT


def writhe_text(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    Question(text, question_type, True)
    context.bot.send_message(update.message.chat_id, strs.operation_success)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    global question_type
    question_type = ''

    message = update.callback_query.message
    context.bot.editMessageText(strs.operation_canceled, chat_id=message.chat_id, message_id=message.message_id)

    return ConversationHandler.END


add_question_conv = ConversationHandler(
    entry_points=[CommandHandler('newquestion', start)],
    states={
        TYPE: [CallbackQueryHandler(choose_type,
                                    pattern='^{};(DARE|TRUTH)$'.format(
                                        CallbackDataType.ADMIN_ADD_QUESTION_TYPE.value))],
        TEXT: [MessageHandler(Filters.text, writhe_text)]
    },
    fallbacks=[CallbackQueryHandler(cancel,
                                    pattern='^{}$'.format(CallbackDataType.ADMIN_ADD_QUESTION_CANCEL.value))],
)
