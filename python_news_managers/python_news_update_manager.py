import datetime


class PythonNewsUpdateManager:

    def __init__(self, db_manager, log_manager=None):
        self._db_manager = db_manager
        self._log_manager = log_manager
        self._news_loaders = []

    def add_news_loader(self, news_loader):
        self._news_loaders.append(news_loader)

    def _get_news_from_loaders(self, last_update_time):
        for news_loader in self._news_loaders:
            try:
                news_from_loader = news_loader.get_news(last_update_time)
            except Exception as e:
                if self._log_manager:
                    self._log_manager.log_message('Error occurred in loader %s: %s' %
                                                  (str(news_loader.__class__.__name__),
                                                str(e)))
                continue

            for news in news_from_loader:
                yield news
            if self._log_manager:
                self._log_manager.log_message('Got news from ' +
                                              str(news_loader.__class__.__name__))

    def _get_actual_news(self, db, last_news_update_time):
        for loaded_news in self._get_news_from_loaders(last_news_update_time):
            for stored_news in db:
                if are_news_similar(loaded_news, stored_news):
                    break
            else:
                db.append(loaded_news)

    def update_news_in_db(self):
        db = self._db_manager.load_db_from_file() or []
        if db:
            last_update_time = max(news['datetime'] for news in db)
        else:
            last_update_time = datetime.datetime.today()\
                .replace(hour=0, minute=0, second=0, microsecond=0) \
                - datetime.timedelta(days=1)

        self._get_actual_news(db, last_update_time)
        self._db_manager.save_db_to_file(db)


def are_news_similar(news1, news2):
    if not news1['link'] and news1['link'] == news2['link']:
        return True
    text1 = '%s %s' % (news1['title'], news1['description'])
    text2 = '%s %s' % (news2['title'], news2['description'])
    count_of_similar_blocks = 0
    for position in range(0, len(text1) - 10, 5):
        if text1[position:position + 10] in text2:
            count_of_similar_blocks += 1
            if count_of_similar_blocks == 5:
                return True
    return False
