import admin_bot
import entities
import main_bot

if __name__ == '__main__':
    entities.load_data()
    main_bot.listen()
    admin_bot.listen()
    print('Ready!')
