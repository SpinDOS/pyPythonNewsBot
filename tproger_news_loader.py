from python_news_html_loader import PythonNewsHtmlLoader
from html_decode_helpers import decode_html
import bs4
import re
import requests
import datetime


class TProgerNewsLoader(PythonNewsHtmlLoader):
    def __init__(self):
        PythonNewsHtmlLoader.__init__(self, 'https://tproger.ru/tag/python/')

    def parse_html_page_to_articles(self, html_page):
        parser = bs4.BeautifulSoup(html_page, 'html.parser')
        main_columns = parser.find("div", {"id": "main_columns"})
        return main_columns.find_all("article", {"class": "item"})

    def get_next_page_link_from_html(self, html_page):
        parser = bs4.BeautifulSoup(html_page, 'html.parser')
        pagination_div = parser.find("div", {"class": "pagination"})
        current_page_html = pagination_div.find("span", {"class": {"current"}})
        next_page_a = current_page_html.findNext("a")
        if not next_page_a or next_page_a.parent != pagination_div:
            return None
        else:
            return next_page_a['href']

    def get_current_article_datetime(self):
        block_with_link_to_article = self.current_article_html.find("h2", {"class": "entry-title"})
        article_url = block_with_link_to_article.a['href']
        article_page = requests.get(article_url).content
        parser = bs4.BeautifulSoup(article_page, "html.parser")
        article_block = parser.find("article", {"id": re.compile("post-*")})
        article_time_string = article_block.find("time", {"class": "entry-date updated"})
        datetime_string = article_time_string['datetime'].partition('+')[0]
        return datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S')

    def get_current_article_info(self):
        current_article = self.current_article_html
        article_info = dict()
        article_info['title'] = decode_html(current_article.find("span", {"class": "entry-title-heading"}))
        article_info['description'] = decode_html(current_article.
                                                  find("div", {"class": "entry-content"}))
        article_info['link'] = current_article.find("h2", {"class": "entry-title"}).a['href']
        return article_info

