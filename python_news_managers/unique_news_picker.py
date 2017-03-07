import datetime
import random
import time


class UniqueNewsPicker(object):
    _UPDATE_TIMEOUT = datetime.timedelta(minutes=30)

    def __init__(self, db_manager, update_manager):
        self._db_manager = db_manager
        self._update_manager = update_manager
        self._actual_news = []
        self._users_sync_blocks = []
        self._last_update_from_db = datetime.datetime(1, 1, 1)
        self._last_old_news_removal = datetime.datetime(1, 1, 1)

    def get_random_actual_news_for_user(self, user_id):
        while user_id in self._users_sync_blocks:
            time.sleep(1)
        self._users_sync_blocks.append(user_id)
        actual_news_for_user = self._choose_actual_news_for_user(user_id)
        if actual_news_for_user:
            news = UniqueNewsPicker._choose_random_news(actual_news_for_user, user_id)
        else:
            news = None
        self._users_sync_blocks.remove(user_id)
        return news

    def get_stored_actual_news_for_user(self, user_id):
        return [news for news in self._actual_news
                if user_id not in news['people']]

    def _choose_actual_news_for_user(self, user_id):
        day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        self._remove_old_news_from_list(day_ago)
        actual_news_for_user = self.get_stored_actual_news_for_user(user_id)
        if actual_news_for_user:
            return actual_news_for_user
        self._update_manager.update_news_in_db()
        self._update_actual_news_list_from_db(day_ago)
        return self.get_stored_actual_news_for_user(user_id)

    def _remove_old_news_from_list(self, date_of_oldest_news):
        now = datetime.datetime.now()
        if self._last_old_news_removal + self._UPDATE_TIMEOUT > now:
            return
        self._last_old_news_removal = now
        for news in self._actual_news:
            if news['datetime'] < date_of_oldest_news:
                self._actual_news.remove(news)

    def _update_actual_news_list_from_db(self, oldest_news_date):
        now = datetime.datetime.now()
        if self._last_update_from_db + self._UPDATE_TIMEOUT > now:
            return
        self._last_update_from_db = now
        for news in self._db_manager.load_db_from_file() or []:
            if news['datetime'] >= oldest_news_date and \
                    not self._is_actual_news_contains_news(news):
                news['people'] = []
                self._actual_news.append(news)

    def _is_actual_news_contains_news(self, news_to_check):
        for news in self._actual_news:
            news_copy = news.copy()
            news_copy.pop('people', None)
            if news_to_check == news_copy:
                return True
        return False

    @staticmethod
    def _choose_random_news(actual_news_for_user, user_id):
        random_index = random.randint(0, len(actual_news_for_user) - 1)
        news = actual_news_for_user[random_index]
        news['people'].append(user_id)
        return news

