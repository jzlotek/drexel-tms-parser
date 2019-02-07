from sdk.crawler.tms_crawler import Crawler
from utils import logger


def run_crawler():
    # try:
    crawler = Crawler(mp=True)
    crawler.crawl()
    # except Exception as ex:
    #     logger.error('{}', ex)


if __name__ == '__main__':
    logger.info("Starting crawler")

    run_crawler()
