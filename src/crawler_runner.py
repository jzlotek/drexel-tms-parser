from crawler.tms_crawler import Crawler
from utils import logger
import multiprocessing


def run_crawler():
    try:
        crawler = Crawler()
        crawler.crawl()
    except Exception as e:
        logger.error('{}'.format(str(e)))


if __name__ == '__main__':
    logger.info("Starting crawler")
    crawler_process = multiprocessing.Process(target=run_crawler)

    try:
        crawler_process.start()
    except Exception as e:
        print(e)
        crawler_process.terminate()
