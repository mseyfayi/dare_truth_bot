from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from entities import Admin
from strings import strings

admin_strings = strings.admin

PASSWORD = range(1)

start_message_id = ''


def start_admin(update: Update, context: CallbackContext):
    message = context.bot.send_message(update.message.chat_id, text=admin_strings.start)
    global start_message_id
    start_message_id = message.message_id
    return PASSWORD


def enter_password(update: Update, context: CallbackContext):
    message = update.message
    context.bot.delete_message(message.chat_id, message.message_id)

    def edit_message(text):
        context.bot.edit_message_text(text, message.chat_id, start_message_id)

    try:
        Admin(message.chat_id, message.text)
        edit_message(admin_strings.password_success)
        return ConversationHandler.END
    except PermissionError:
        edit_message(admin_strings.password_retry)
        return PASSWORD


start_conv = ConversationHandler(
    entry_points=[CommandHandler('start', start_admin)],
    states={
        PASSWORD: [MessageHandler(Filters.text, enter_password)]
    },
    fallbacks=[],
)
