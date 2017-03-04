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
    current_post_text = None

    def clear_cache(self):
        self.__posts = []
        self.__current_index = -1
        self.__start_from = None
        self.current_post = None
        self.current_post_text = None

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
            current_post = self.__posts[self.__current_index]
            self.current_post = current_post
            self.current_post_text = get_post_and_ancestors_text(current_post)
            if is_text_contains_python_news(self.current_post['text']):
                return True

    def get_current_article_datetime(self):
        return datetime.datetime.fromtimestamp(self.current_post['date'])

    def __get_posts(self):
        params_of_request = {
            'q': self.SEARCH_WORD,
            'extended': 1,
            'count': self.NUM_OF_POSTS_IN_SINGLE_REQUEST,
        }
        if self.__start_from:
            params_of_request['start_from'] = self.__start_from
        vk_response = make_vk_api_request(self.SEARCH_METHOD, params_of_request)
        self.__posts = vk_response['items']
        self.__start_from = vk_response.get('next_from', None)
        self.__current_index = -1

    def get_current_article_title(self):
        return self.current_post_text.partition('\n')[0]

    def get_current_article_description(self):
        return self.current_post_text.partition('\n')[2]

    def get_current_article_link(self):
        return generate_link_by_owner_and_id(self.current_post['owner_id'],
                                             self.current_post['id'])


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
        prev_post = make_vk_api_request('wall.getById', params)[0]
        text = '%s\n%s' % (text, prev_post['text'])
    return text


def is_text_contains_python_news(text):
    text = text.lower()
    not_news_words_combination = [
        ['приглаш', 'обучени'],     # реклама курсов
        ['приглаш', 'курс'],        # по программированию
        ['курс программирования'],  # на питоне
        ['кож', 'цвет'],    # одежда
        ['кож', 'размер'],  # и обувь
        ['кож', 'стил'],    # из кожи
        ['одежд'],          # питона 
        ['обув'],           # (змеи)
        ['#snake'],  # просто новости про змей
        ['заказ', 'бесплатн'],  # услуги
        ['недорог'],            # по программированию
        ['скидк'],              # на питоне
        ['с днём рождения'],  # хз вообще откуда это находится, но таких постов много
        ['#trianglesis'],  # постоянно появляется мусор с этим тэгом

    ]

    for collection_of_bad_words in not_news_words_combination:
        count_of_bad_words_in_text = 0
        for bad_word in collection_of_bad_words:
            if bad_word in text:
                count_of_bad_words_in_text += 1
        if count_of_bad_words_in_text == len (collection_of_bad_words):
            return False
    return True
