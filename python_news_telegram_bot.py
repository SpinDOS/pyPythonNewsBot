#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import logging
import os
import sys
import python_news_update
from python_news_update_managers.python_news_db_manager import PythonNewsDbManager
from unique_news_picker import UniqueNewsPicker

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def run_telegram_bot(telegram_token):
    updater = Updater(telegram_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("python_news", python_news))
    dp.add_handler(MessageHandler(Filters.text, help))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


def start(bot, update):
    update.message.reply_text('Hello, I am Alexander Platonov\'s bot! '
                              'Say \'/python_news\' to get news about Python!')


def help(bot, update):
    update.message.reply_text('Say \'/python_news\' to get news about Python!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def configure_message(news):
    return '%s \n%s \nSource: %s' % (news['title'], news['description'],
                                     news['link'])


def python_news(bot, update):
    user_id = update['message']['chat']['id']
    actual_news = _unique_news_picker.get_random_actual_news_for_user(user_id)
    if not actual_news:
        update.message.reply_text('Sorry, no actual news available. Try later')
        return
    message = configure_message(actual_news)
    update.message.reply_text(message)


_unique_news_picker = None

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Usage: python python_news_telegram_bot.py <news_db_file_path>")
    else:
        db_filename = sys.argv[1] if len(sys.argv) == 2 else 'python_news_db.json'
        db_manager = PythonNewsDbManager(db_filename)
        news_update_manager = python_news_update.configure_update_manager(db_manager, None)
        _unique_news_picker = UniqueNewsPicker(db_manager, news_update_manager)
        telegram_api_token = os.environ.get('TELEGRAM_API_TOKEN')
        if telegram_api_token:
            print("Working... Press Ctrl+C to stop")
            run_telegram_bot(telegram_api_token)
        else:
            print("Set telegram api token for your bot (contact BotFather on Telegram) "
                  "as an environment variable TELEGRAM_API_TOKEN")