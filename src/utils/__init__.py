from loguru import logger
import sys

class Logger:
    @staticmethod
    def logger():
        return logger

logger = Logger().logger()