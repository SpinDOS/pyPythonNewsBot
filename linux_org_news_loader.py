from python_news_html_loader import PythonNewsHtmlLoader
from html_decode_helpers import decode_html
import datetime
import bs4


class LinuxOrgNewsLoader(PythonNewsHtmlLoader):

    def __init__(self):
        PythonNewsHtmlLoader.__init__(self, 'https://www.linux.org.ru/tag/python?section=1')

    def parse_html_page_to_articles(self, html_page):
        parser = bs4.BeautifulSoup(html_page, 'html.parser')
        main_block = parser.find("div", {"id": "bd"})
        return main_block.find_all("article", {"class": "news"})

    def get_next_page_link_from_html(self, html_page):
        parser = bs4.BeautifulSoup(html_page, 'html.parser')
        next_page_nav = parser.find("table", {"class": "nav"})
        relative_url = next_page_nav.find("a")['href']
        return 'https://www.linux.org.ru' + relative_url

    def get_current_article_datetime(self):
        article_time_html = self.current_article_html.find("div", {"class": "sign"}).time
        datetime_string = article_time_html['datetime'].partition('.')[0]
        return datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S')

    def get_current_article_info(self):
        current_article = self.current_article_html
        article_info = dict()
        article_info['title'] = decode_html(current_article.h2.a.string)
        article_body_html = current_article.find("div", {"class": "msg"})
        article_descriptors = article_body_html.find_all("p")
        article_info['description'] = decode_html(article_descriptors[0])
        article_info['link'] = article_descriptors[-1].a['href']
        return article_info
