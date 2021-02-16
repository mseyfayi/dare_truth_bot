# Dare Truth Telegram Bot
## About The Bot
A telegram bot that presents [dare or truth game](https://en.wikipedia.org/wiki/Truth_or_dare%3F) (بازی جرات یا حقیقت) on [telegram  app](https://telegram.org/)
### How to use
- Open the [bot](https://telegram.me/d4r37ruth_bot)
- Start bot or type "/start" as a command
- Tap "Game" or "بازی" button
- Choose a chat (a private chat or a group)
- Tap on "Send" or "ارسال" button in shown dialog
- Wait until other people join the game by tapping "I'm in too" or "منم هستم" button
- Tap "Start" or "شروع" button
- The game will choose a member to answer randomly \
He/She will have two choice, "Dare" and "Truth" or "جرات" and "حقیقت" 
- The will pick a question to answer (for truth) or a job to do (for dare)
- After answering the question or doing the job, tap "Answered" or "جواب دادم"
- Game will choose next person (It may be repetitive)
- ...
### Upcoming Features
- Help button
- Admin bot to accept or reject suggested questions
- "Move to down" button
- "Skip" button
- Vote to convince the other members of the answer
- Add second language
## How To Run
#### Configure Environment Variables
Create .env file
```commandline
touch .env
```
Fill .env file
```.env
ENV=development | production

MONGO_DBNAME= "Mongodb collection name"
MONGO_USER= "Mongodb username"
MONGO_PASS= "Mongodb password"
MONGO_CLUSTER= "Mongodb cluster address for production (Mongodb Atlas)"

BOT_TOKEN= "Token of Telegram Bot"
```
#### Install Dependencies
```commandline
pip install -r requirements.txt
```
#### Run The Script
```commandline
python main.py
```
Use the bot :)

