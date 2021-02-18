from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

from bot.callback_data import CallbackDataType, restore_callback_data
from bot.commands import start_reply_markup
from entities.question import Question
from strings import strings
from utils import build_menu, create_inline_button

TYPE, TEXT = range(2)

conv_strings = strings.conversations

question_type = ''


def send_question(update: Update, context: CallbackContext) -> int:
    send_string = conv_strings.send_question_type
    button_list = [create_inline_button(send_string.buttons, t,
                                        callback_data_name='send_question_type',
                                        callback_data_creator_payload=t.upper())
                   for t in send_string.buttons.keys()]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    context.bot.send_message(update.callback_query.message.chat_id, send_string.text, reply_markup=reply_markup)

    return TYPE


def choose_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    data = query.data
    ignore, [q_type] = restore_callback_data(data)
    global question_type
    question_type = str(q_type).lower()
    context.bot.editMessageText(conv_strings.enter_question_text, inline_message_id=query.inline_message_id)

    return TEXT


def writhe_text(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    # todo send to admin
    Question(text, question_type)
    context.bot.editMessageText(conv_strings.send_question_success,
                                inline_message_id=update.callback_query.inline_message_id,
                                reply_markup=start_reply_markup)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    global question_type
    question_type = ''
    context.bot.editMessageText(conv_strings.send_question_success,
                                inline_message_id=update.callback_query.inline_message_id,
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
                                    pattern='^{};(DARE|TRUTH)$'.format(CallbackDataType.SEND_QUESTION_TYPE.value))],
)
