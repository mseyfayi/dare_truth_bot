import admin_bot
import main_bot
from entities.admin import Admin
from entities.game import Game
from entities.question import Question
from entities.user import MyUser


def load_data():
    MyUser.load_all()
    Question.load_all()
    Game.load_all()
    Admin.load_all()
    print("Games: ", Game.instances)
    print("MyUser: ", MyUser.instances)
    print("Question: ", Question.instances)
    print("Admin: ", Admin.instances_list)


if __name__ == '__main__':
    load_data()
    main_bot.listen()
    admin_bot.bot_listen()
    admin_bot.question_listen()
    print('Ready!')
