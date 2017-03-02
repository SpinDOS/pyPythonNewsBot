from abc import abstractmethod
import requests
from python_news_loader import PythonNewsLoader


class PythonNewsHtmlLoader(PythonNewsLoader):

    __site_url = ''
    __html_articles_collection = []
    __current_index = -1
    __next_page_link = None
    current_article_html = ''

    def __init__(self, html_site_url):
        self.__site_url = html_site_url

    def update_news(self):
        self.__get_articles_from_url(self.__site_url)

    def move_next(self):
        if self.__current_index + 1 == len(self.__html_articles_collection):
            if not self.__next_page_link:
                return False
            else:
                self.__get_articles_from_url(self.__next_page_link)

        self.__current_index += 1
        self.current_article_html = self.__html_articles_collection[self.__current_index]
        return True

    def clear_cache(self):
        self.__html_articles_collection = []
        self.__current_index = -1
        self.__next_page_link = None
        self.current_article_html = ''

    def __get_articles_from_url(self, url):
        html_page = requests.get(url).content
        self.__html_articles_collection = self.parse_html_page_to_articles(html_page)
        self.__next_page_link = self.get_next_page_link_from_html(html_page)
        self.__current_index = -1

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
    def get_current_article_info(self):
        pass
