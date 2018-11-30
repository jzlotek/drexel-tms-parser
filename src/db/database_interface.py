import abc
import logging


class Database(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def create_table(self, table_name, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_table(self, table_name, *args, **kwargs):
        pass

    @abc.abstractmethod
    def update_data(self, table_name, data, *args, **kwargs):
        pass

    @abc.abstractmethod
    def find_one(self, table_name, query, *args, **kwargs):
        pass

    @abc.abstractmethod
    def find_many(self, table_name, query, *args, **kwargs):
        pass

    @abc.abstractmethod
    def insert(self, table_name, data, *args, **kwargs):
        pass

    def logger(self):
        return logging.getLogger(self)
