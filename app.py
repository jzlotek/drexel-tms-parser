from flask import Flask, render_template
import datetime
import multiprocessing
import os
from src.crawler.tms_crawler import Crawler


def run_crawler():
    try:
        crawler = Crawler()
        crawler.crawl()
    except Exception as e:
        print('\n\n{}\n\n{}\n\n'.format(str(e), str(datetime.datetime.now())))


app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("./dist/index.html")


if __name__ == '__main__':

    if 'dist' not in os.listdir('./'):
        os.mkdir('./dist')

    if '.tmp' not in os.listdir('./dist'):
        os.mkdir('./dist/.tmp')


    crawler_process = multiprocessing.Process(target=run_crawler)

    try:
        crawler_process.start()
        app.run(debug=True)
    except Exception as e:
        print(e)
        crawler_process.terminate()
