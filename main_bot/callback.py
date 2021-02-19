from typing import Optional, Dict

from telegram import Update, ReplyMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from main_bot.callback_data import CallbackDataType, restore_callback_data
from main_bot.inline import create_inline_markup
from entities.game import Game
from entities.user import MyUser
from strings import strings
from utils import create_inline_button, build_menu

callback_strings = strings.callbacks


def create_bot_link_button(link: str):
    return InlineKeyboardButton(callback_strings.bot_link_btn, url=link)


def create_buttons(game_id: str, link: str, buttons: Dict, is_attach_key: bool = True):
    payload = "{}".format(game_id)
    button_list = [create_inline_button(buttons, t,
                                        callback_data_creator_payload=(payload + ';' + t) if is_attach_key else payload)
                   for t in buttons.keys()]

    reply_markup = InlineKeyboardMarkup(
        build_menu(button_list, n_cols=2, footer_buttons=[create_bot_link_button(link)]))
    return reply_markup


def create_choice_markup(game_id: str, link: str) -> ReplyMarkup:
    buttons = callback_strings.choose_type.buttons

    return create_buttons(game_id, link, buttons)


def create_vote_markup(game_id: str, link: str) -> ReplyMarkup:
    buttons = callback_strings.vote.buttons

    return create_buttons(game_id, link, buttons)


def create_question_markup(game_id: str, link: str):
    buttons = callback_strings.question.buttons

    return create_buttons(game_id, link, buttons, False)


def callback(update: Update, context: CallbackContext):
    link = context.bot.link
    query = update.callback_query
    user = query.from_user
    data = query.data
    not_found_alert = callback_strings.not_found_alert

    def alert(text: str):
        context.bot.answer_callback_query(callback_query_id=query.id, text=text, show_alert=True)

    def edit_message(text: str, reply_markup: Optional[ReplyMarkup] = None):
        context.bot.editMessageText(text, inline_message_id=query.inline_message_id, reply_markup=reply_markup)

    print("received: ", data)
    data_type, payloads = restore_callback_data(data)
    if CallbackDataType.HELP.value == data_type:
        alert(not_found_alert)
    elif CallbackDataType.GET_IN.value == data_type:
        [game_id] = payloads
        game = Game.get_instance(game_id)

        def edit_game_inline():
            edit_message(callback_strings.before_start(game), create_inline_markup(game))

        game.get_in(MyUser.new(user.id, user.first_name), alert, edit_game_inline)
    elif CallbackDataType.START.value == data_type:
        [game_id] = payloads
        starter_id = user.id
        game = Game.get_instance(game_id)

        def edit_game_inline():
            edit_message(callback_strings.choose_type.text(game), create_choice_markup(game_id, link))

        game.start(starter_id, alert, edit_game_inline)
    elif CallbackDataType.CHOOSE.value == data_type:
        [game_id, q_type] = payloads
        user_id = user.id
        game = Game.get_instance(game_id)

        def edit_question():
            edit_message(callback_strings.question.text(game), create_question_markup(game_id, link))

        game.choose(user_id, q_type, alert, edit_question)
    elif CallbackDataType.ANSWER.value == data_type:
        [game_id] = payloads
        user_id = user.id
        game = Game.get_instance(game_id)

        def edit_vote():
            edit_message(callback_strings.vote.text(game), create_vote_markup(game_id, link))

        game.answer(user_id, alert, edit_vote)
    elif CallbackDataType.VOTE.value == data_type:
        [game_id, result] = payloads
        user_id = user.id
        game = Game.get_instance(game_id)

        def edit(is_voting_finish: bool, is_repeated: bool):
            if is_repeated:
                text = callback_strings.question.text(game, is_repeated)
                markup = create_question_markup(game_id, link)
            elif is_voting_finish:
                text = callback_strings.choose_type.text(game)
                markup = create_choice_markup(game_id, link)
            else:
                text = callback_strings.vote.text(game)
                markup = create_vote_markup(game_id, link)
            edit_message(text, markup)

        game.vote(user_id, result, alert, edit)
    else:
        alert(callback_strings.not_recognized)
