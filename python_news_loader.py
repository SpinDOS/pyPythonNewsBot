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
    def get_current_article_title(self):
        pass

    @abstractmethod
    def get_current_article_description(self):
        pass

    @abstractmethod
    def get_current_article_link(self):
        pass

    def __get_current_article_info(self):
        article_info = dict()
        article_info['title'] = self.get_current_article_title()
        article_info['description'] = self.get_current_article_description()
        article_info['link'] = self.get_current_article_link()
        return article_info

    def get_news(self, datetime_of_latest_article = datetime.datetime.today().
                 replace(hour=0, minute=0, second=0, microsecond=0)):
        self.update_news()
        articles = []
        while self.move_next():
            current_article_datetime = self.get_current_article_datetime()
            if current_article_datetime < datetime_of_latest_article:
                break
            current_article_info = self.__get_current_article_info()
            current_article_info['datetime'] = current_article_datetime
            articles.append(current_article_info)
        self.clear_cache()
        return articles
