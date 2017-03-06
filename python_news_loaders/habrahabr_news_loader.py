import datetime

import bs4

from helper_methods.html_decode_helpers import decode_html
from python_news_loaders.python_news_html_loader import PythonNewsHtmlLoader


class HabraHabrNewsLoader(PythonNewsHtmlLoader):

    def __init__(self):
        PythonNewsHtmlLoader.__init__(self, 'https://habrahabr.ru/hub/python/')

    def parse_html_page_to_articles(self, html_page):
        parser = bs4.BeautifulSoup(html_page, 'html.parser')
        posts = parser.find("div", {"class": "posts_list"}) \
            .find("div", {"class": "posts"})
        return posts.find_all("div", {"class": "post"})

    def get_next_page_link_from_html(self, html_page):
        parser = bs4.BeautifulSoup(html_page, 'html.parser')
        next_page_link = parser.find("a", {"id": "next_page"})
        if not next_page_link:
            return None
        else:
            return 'https://habrahabr.ru' + next_page_link['href']

    def get_current_article_datetime(self):
        datetime_string = decode_html(self.current_article_html.find("span",
                                                     {"class" : "post__time_published"}))
        date_and_time = datetime_string.replace('\n', '').strip().split(' в ')
        return get_date_from_string(date_and_time[0]) + \
               get_time_from_string(date_and_time[1])

    def get_current_article_title(self):
        title_link = self.current_article_html.find("a", {"class": "post__title_link"})
        return decode_html(title_link)

    def get_current_article_description(self):
        return decode_html(self.current_article_html.find("div", {"class": "post__body"}).div)

    def get_current_article_link(self):
        title_link = self.current_article_html.find("a", {"class": "post__title_link"})
        return title_link['href']


def month_string_to_int(month):
    return {
        "января": 1, "февраля": 2, "марта": 3, "апреля": 4,
        "мая": 5, "июня": 6, "июля": 7, "августа": 8,
        "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
    }[month]


def get_date_from_string(date_string):
    if 'сегодня' in date_string:
        return datetime.datetime.today()
    if 'вчера' in date_string:
        return datetime.datetime.today() - datetime.timedelta(days=1)
    date_parts = date_string.split()
    day = int(date_parts[0])
    month = month_string_to_int(date_parts[1])

    if len(date_parts) > 2:
        year = int(date_parts[2])
    else:
        year = datetime.datetime.today().year
    return datetime.datetime(year=year, month=month, day=day)


def get_time_from_string(time_string):
    hour_and_minute = time_string.split(':')
    hour = int(hour_and_minute[0])
    minute = int(hour_and_minute[1])
    return datetime.timedelta(hours=hour, minutes=minute)
