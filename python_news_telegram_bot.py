#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import sys
import datetime
import random
import time
from python_news_db_manager import PythonNewsDbManager
import python_news_update

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


def is_actual_news_contains_news(news_to_check):
    for news in _actual_news:
        news_copy = news.copy()
        news_copy.pop('people', None)
        if news_to_check == news_copy:
            return True
    return False


def remove_old_news_from_list(date_of_oldest_news):
    if _db_and_list_sync_blocks[1]:
        while _db_and_list_sync_blocks[1]:
            time.sleep(1)
        return
    _db_and_list_sync_blocks[1] = True
    for news in _actual_news:
        if news['datetime'] < date_of_oldest_news:
            _actual_news.remove(news)
    _db_and_list_sync_blocks[1] = False


def update_news_in_lists_from_db(oldest_news_date):
    if _db_and_list_sync_blocks[0]:
        while _db_and_list_sync_blocks[0]:
            time.sleep(1)
        return
    _db_and_list_sync_blocks[0] = True
    for news in _db_manager.load_db_from_file() or []:
        if news['datetime'] >= oldest_news_date and \
                not is_actual_news_contains_news(news):
            news['people'] = []
            _actual_news.append(news)
    _db_and_list_sync_blocks[0] = False


def get_stored_actual_news_for_user(user_id):
    return [news for news in _actual_news
            if user_id not in news['people']]


def get_actual_news_for_user(user_id):
    day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    remove_old_news_from_list(day_ago)
    actual_news_for_user = get_stored_actual_news_for_user(user_id)
    if actual_news_for_user:
        return actual_news_for_user
    _news_update_manager.update_news_in_db()
    update_news_in_lists_from_db(day_ago)
    return get_stored_actual_news_for_user(user_id)


def choose_random_news(actual_news_for_user, user_id):
    random_index = random.randint(0, len(actual_news_for_user) - 1)
    news = actual_news_for_user[random_index]
    news['people'].append(user_id)
    return news


def configure_message(news):
    return '%s \n%s \nSource: %s' % (news['title'], news['description'],
                                     news['link'])


def python_news(bot, update):
    user_id = update['message']['chat']['id']
    while user_id in _users_sync_blocks:
        time.sleep(1)
    _users_sync_blocks.append(user_id)
    actual_news_for_user = get_actual_news_for_user(user_id)
    if not actual_news_for_user:
        update.message.reply_text('Sorry, no actual news available. Try later')
    else:
        news = choose_random_news(actual_news_for_user, user_id)
        message = configure_message(news)
        update.message.reply_text(message)
    _users_sync_blocks.remove(user_id)

_db_and_list_sync_blocks = [False, False]
_users_sync_blocks = []
_actual_news = []
_db_manager = None
_news_update_manager = None


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Usage: python python_news_telegram_bot.py <news_db_file_path>")
    else:
        db_filename = sys.argv[1] if len(sys.argv) == 2 else 'python_news_db.json'
        _db_manager = PythonNewsDbManager(db_filename)
        _news_update_manager = python_news_update.configure_update_manager(_db_manager, None)
        telegram_api_token = os.environ.get('TELEGRAM_API_TOKEN')
        if telegram_api_token:
            print("Working... Press Ctrl+C to stop")
            run_telegram_bot(telegram_api_token)
        else:
            print("Set telegram api token for your bot (contact BotFather on Telegram) "
                  "as an environment variable TELEGRAM_API_TOKEN")