import admin_bot
import entities
import main_bot

if __name__ == '__main__':
    entities.load_data()
    main_bot.listen()
    admin_bot.bot_listen()
    admin_bot.question_listen()
    print('Ready!')
