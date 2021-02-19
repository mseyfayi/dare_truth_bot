from telegram import Update
from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext

from callback_data import CallbackDataType
from entities.question import Question

SHOW_QUESTION, = range(1)


def next_question():
    inactive_questions = [q for q in Question.instances.values() if not q.is_active]
    yield inactive_questions


def show_question(update: Update, context: CallbackContext) -> int:
    # todo confirm or refuse or skip
    question = next_question()
    if question:
        # todo show next question
        return SHOW_QUESTION
    else:
        # todo done
        return ConversationHandler.END


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
