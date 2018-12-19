from loguru import logger


class Logger:
    @staticmethod
    def logger():
        """
        Define config for loguru logger here.
        Gets used by:
        `from utils import logger`
        :return: logger
        """
        return logger


logger = Logger().logger()
