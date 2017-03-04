#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import sys
import datetime
import random
from python_news_db_manager import PythonNewsDbManager
from python_news_update import configure_update_manager

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hello, I am Alexander Platonov\'s bot! '
                              'Say \'/python_news\' to get news about Python!')


def help(bot, update):
    update.message.reply_text('Say \'/python_news\' to get news about Python!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


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


def remove_old_news_from_lists(date_of_old_news):
    for news in actual_news:
        if news['datetime'] < date_of_old_news:
            actual_news.remove(news)
    for news in used_news:
        if news['datetime'] < date_of_old_news:
            used_news.remove(news)


def update_news_in_lists_from_db(oldest_news_date):
    for news in db_manager.load_db_from_file() or []:
        if news['datetime'] >= oldest_news_date and \
                        news not in actual_news + used_news:
            actual_news.append(news)


def update_actual_news():
    day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    remove_old_news_from_lists(day_ago)
    if actual_news:
        return
    news_update_manager = configure_update_manager(db_manager, None)
    news_update_manager.update_news()
    update_news_in_lists_from_db(day_ago)


def choose_random_news():
    random_index = random.randint(0, len(actual_news) - 1)
    news = actual_news.pop(random_index)
    used_news.append(news)
    return news


def configure_message(news):
    return '%s \n%s \nSource: %s' % (news['title'], news['description'],
                                      news['link'])


def python_news(bot, update):
    while sync_block[0]:
        pass
    sync_block[0] = 1
    update_actual_news()
    if not actual_news:
        update.message.reply_text('Sorry, no actual news available. Try later')
        sync_block[0] = 0
        return
    message = configure_message(choose_random_news())
    update.message.reply_text(message)
    sync_block[0] = 0

sync_block = [0]
actual_news = []
used_news = []
db_manager = None


if __name__ == '__main__':
    db_filename = sys.argv[1] if len(sys.argv) == 2 else 'python_news_db.json'
    db_manager = PythonNewsDbManager(db_filename)
    telegram_api_token = os.environ.get('TELEGRAM_API_TOKEN')
    telegram_api_token = '301168706:AAFe-xdTCXgnubduBH7xZ4l4YT9VoYranQ0'
    if telegram_api_token:
        print("Working...")
        run_telegram_bot(telegram_api_token)
    else:
        print("Set telegram api token for your bot (contact BotFather on Telegram) "
              "as an environment variable TELEGRAM_API_TOKEN")