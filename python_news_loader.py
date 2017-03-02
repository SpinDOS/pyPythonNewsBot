import datetime
from abc import ABC, abstractmethod


class PythonNewsLoader(ABC):

    @abstractmethod
    def clear_cache(self):
        pass

    @abstractmethod
    def update_news(self):
        pass

    @abstractmethod
    def move_next(self):
        pass

    @abstractmethod
    def get_current_article_datetime(self):
        pass

    @abstractmethod
    def get_current_article_info(self):
        pass

    def get_news(self, datetime_of_latest_article = datetime.datetime.today().
                 replace(hour=0, minute=0, second=0, microsecond=0)):
        self.update_news()
        articles = []
        while self.move_next():
            if self.get_current_article_datetime() < datetime_of_latest_article:
                break
            articles.append(self.get_current_article_info())
        self.clear_cache()
        return articles
