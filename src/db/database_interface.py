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

    def logger(self):
        return logging.getLogger(str(self))
