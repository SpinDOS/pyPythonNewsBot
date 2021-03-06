from abc import abstractmethod

import requests

from python_news_loaders.python_news_loader import PythonNewsLoader


class PythonNewsHtmlLoader(PythonNewsLoader):

    def __init__(self, html_site_url):
        self._site_url = html_site_url
        self._html_articles_collection = []
        self._current_index = -1
        self._next_page_link = None
        self.current_article_html = ''

    def update_news(self):
        self._get_articles_from_url(self._site_url)

    def move_next(self):
        if self._current_index + 1 == len(self._html_articles_collection):
            if not self._next_page_link:
                return False
            else:
                self._get_articles_from_url(self._next_page_link)

        self._current_index += 1
        self.current_article_html = self._html_articles_collection[self._current_index]
        return True

    def clear_cache(self):
        self._html_articles_collection = []
        self._current_index = -1
        self._next_page_link = None
        self.current_article_html = ''

    def _get_articles_from_url(self, url):
        html_page = requests.get(url).content
        self._html_articles_collection = self.parse_html_page_to_articles(html_page)
        self._next_page_link = self.get_next_page_link_from_html(html_page)
        self._current_index = -1

    @abstractmethod
    def parse_html_page_to_articles(self, html_page):
        pass

    @abstractmethod
    def get_next_page_link_from_html(self, html_page):
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
