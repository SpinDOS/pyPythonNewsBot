from python_news_loader import PythonNewsLoader
from vk_api_helpers import make_vk_api_request
import datetime


class VkNewsLoader(PythonNewsLoader):

    NUM_OF_POSTS_IN_SINGLE_REQUEST = 10
    SEARCH_WORD = '#python'
    SEARCH_METHOD = 'newsfeed.search'

    __posts = []
    __current_index = -1
    __start_from = None
    current_post = None

    def clear_cache(self):
        self.__posts = []
        self.__current_index = -1
        self.__start_from = None
        self.current_post = None

    def update_news(self):
        self.__get_posts()

    def move_next(self):
        while True: # check all posts until python news found
            if self.__current_index + 1 == len(self.__posts):
                if not self.__start_from:
                    return False
                else:
                    self.__get_posts()

            self.__current_index += 1
            self.current_post = self.__posts[self.__current_index]
            if is_text_contains_python_news(self.current_post['text']):
                return True

    def get_current_article_datetime(self):
        return datetime.datetime.fromtimestamp(self.current_post['date'])

    def get_current_article_info(self):
        post = self.current_post
        article_info = dict()
        text = get_post_and_ancestors_text(post)
        article_info['title'], not_used, article_info['description'] = \
                                                            text.partition('\n')
        if len(article_info['description']) > 100:
            article_info['description'] = article_info['description'][:100] + '...'
        article_info['link'] = generate_link_by_owner_and_id(post['owner_id'],
                                                             post['id'])
        return article_info

    def __get_posts(self):
        params_of_request = {
            'q': self.SEARCH_WORD,
            'extended': 1,
            'count': self.NUM_OF_POSTS_IN_SINGLE_REQUEST,
        }
        if self.__start_from:
            params_of_request['start_from'] = self.__start_from
        vk_response = make_vk_api_request(self.SEARCH_METHOD, params_of_request)['response']
        self.__posts = vk_response['items']
        self.__start_from = vk_response.get('next_from', None)
        self.__current_index = -1


def generate_link_by_owner_and_id(owner_id, id):
    return 'https://vk.com/wall%s_%s' % (owner_id, id)


def get_post_and_ancestors_text(post):
    text = post['text']
    history = post.get('copy_history', None)
    if not history:
        return text
    for prev_post_info in history:
        params = {
            'posts': '%s_%s' % (prev_post_info['owner_id'], prev_post_info['id']),
            'copy_history_depth': 0
        }
        prev_post = make_vk_api_request('wall.getById', params)['response'][0]
        text = '%s\n%s' % (text, prev_post['text'])
    return text


def is_text_contains_python_news(text):
    text = text.lower()
    not_news_words_combination = [
        ['приглаш', 'обучени'],    # реклама курсов
        ['приглаш', 'курс'],       # по программированию
        ['курс программирования'], # на питоне
        ['кож', 'цвет'],   # одежда
        ['кож', 'размер'], # из кожи
        ['кож', 'стил'],   # питона (змеи)
        ['заказ', 'бесплатн'], # услуги
        ['недорог'],           # по программированию
        ['скидк'],             # на питоне
        ['с днём рождения'] # хз вообще откуда это находится, но таких постов много
    ]

    for collection_of_bad_words in not_news_words_combination:
        count_of_bad_words_in_text = 0
        for bad_word in collection_of_bad_words:
            if bad_word in text:
                count_of_bad_words_in_text += 1
        if count_of_bad_words_in_text == len (collection_of_bad_words):
            return False
    return True
