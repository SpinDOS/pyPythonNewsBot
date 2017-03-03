#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hello, I am Alexander Platonov\' bot! '
                              'Say \'\\python_news\' to get news about Python!')


def help(bot, update):
    update.message.reply_text('Say \'\\python_news\' to get news about Python!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main(telegram_token):
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("python_news", python_news))

    # on noncommand answer help
    dp.add_handler(MessageHandler(Filters.text, help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def python_news(bot, update):
    update.message.reply_text('')

if __name__ == '__main__':
    telegram_api_token = os.environ.get('TELEGRAM_API_TOKEN')
    if telegram_api_token:
        main(telegram_api_token)
    else:
        print("Set telegram api token for your bot (contact BotFather on Telegram) "
              "as an environment variable TELEGRAM_API_TOKEN")