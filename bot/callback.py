from typing import Optional

from telegram import Update, ReplyMarkup, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.callback_data import CallbackDataType, _restore_callback_data
from bot.inline import create_inline_markup
from entities.game import Game
from entities.question import Question
from strings import strings
from entities.user import MyUser
from utils import create_inline_button, build_menu

callback_strings = strings.callbacks


def create_choice_markup(game_id: int) -> ReplyMarkup:
    buttons = callback_strings.edit_text2.buttons
    payload = "{}".format(game_id)
    button_list = [create_inline_button(buttons, t, callback_data_creator_payload=payload) for t in buttons.keys()]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup


def create_question_markup(game_id:int):
    buttons = callback_strings.edit_text3.buttons
    payload = "{}".format(game_id)
    button_list = [create_inline_button(buttons, t, callback_data_creator_payload=payload) for t in buttons.keys()]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup


def callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data
    not_found_alert = callback_strings.not_found_alert

    def alert(text: str):
        context.bot.answer_callback_query(callback_query_id=query.id, text=text, show_alert=True)

    def edit_message(text: str, reply_markup: Optional[ReplyMarkup] = None):
        context.bot.editMessageText(text, inline_message_id=query.inline_message_id, reply_markup=reply_markup)

    print("received: ", data)
    data_type, payloads = _restore_callback_data(data)
    if CallbackDataType.HELP.value == data_type:
        alert(not_found_alert)
    elif CallbackDataType.SEND_QUESTION.value == data_type:
        alert(not_found_alert)
    elif CallbackDataType.GET_IN.value == data_type:
        [game_id] = payloads
        game = Game.get_instance(game_id)

        def edit_game_inline():
            edit_message(callback_strings.edit_text1(game), create_inline_markup(game))

        game.get_in(MyUser.new(user.id, user.first_name), alert, edit_game_inline)
    elif CallbackDataType.START.value == data_type:
        [game_id] = payloads
        starter_id = user.id
        game = Game.get_instance(game_id)

        def edit_game_inline():
            edit_message(callback_strings.edit_text2.text(game), create_choice_markup(game_id))

        game.start(starter_id, alert, edit_game_inline)
    elif CallbackDataType.CHOOSE.value == data_type:
        [game_id] = payloads
        user_id = user.id
        game = Game.get_instance(game_id)

        def edit_question(user: MyUser, question: Question):
            # edit_message(callback_strings.edit_text3.text(game, question.type, question.text),
            #              create_question_markup(game_id))
            #  todo
            pass

        game.choose(user_id, alert, edit_question)
    else:
        print("koft1")
