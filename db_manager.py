import json
import os


class DbManager:
    __db_file_path = ''

    def __init__(self, db_file_path):
        self.__db_file_path = db_file_path

    def load_db_from_file(self):
        if not os.path.exists(self.__db_file_path):
            return None
        with open(self.__db_file_path, 'r') as db_file:
            return json.load(db_file)

    def save_db_to_file(self, db):
        with open(self.__db_file_path, 'w') as db_file:
            json.dump(db, db_file)
