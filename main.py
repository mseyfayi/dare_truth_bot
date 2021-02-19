import entities
import main_bot

if __name__ == '__main__':
    entities.load_data()
    main_bot.listen()
