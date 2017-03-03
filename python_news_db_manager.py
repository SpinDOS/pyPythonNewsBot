import json
import os
import datetime


class PythonNewsDbManager:
    __DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'
    __db_file_path = ''

    def __init__(self, db_file_path):
        self.__db_file_path = db_file_path

    def load_db_from_file(self):
        if not os.path.exists(self.__db_file_path):
            return None
        with open(self.__db_file_path, 'r') as db_file:
            db = json.load(db_file)
        for news in db:
            news['datetime'] = \
                datetime.datetime.utcfromtimestamp(news['datetime'])
        return db

    def save_db_to_file(self, db):
        utc_datetime_start = datetime.datetime(1970, 1, 1)
        for news in db[:]:
            news['datetime'] = (news['datetime'] - utc_datetime_start)\
                .total_seconds()
        with open(self.__db_file_path, 'w') as db_file:
            json.dump(db, db_file)
