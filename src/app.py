from flask import Flask, render_template
import datetime
import multiprocessing
import os
from crawler.tms_crawler import Crawler
from db import database



def run_crawler():
    try:
        crawler = Crawler()
        crawler.crawl()
    except Exception as e:
        print('\n\n{}\n\n{}\n\n'.format(str(e), str(datetime.datetime.now())))


app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return render_template("../dist/index.html")

@app.route('/course/<path:path>', methods=['GET'])
def get_course(path):
    print(path)
    database.execute()
    return path


if __name__ == '__main__':
    database.subject_code("CS")
    print(database.execute())
    # database.execute()
    if 'dist' not in os.listdir('../'):
        os.mkdir('../dist')

    if '.tmp' not in os.listdir('../dist'):
        os.mkdir('../dist/.tmp')


    # crawler_process = multiprocessing.Process(target=run_crawler)

    try:
        # crawler_process.start()
        app.run(debug=True)
    except Exception as e:
        print(e)
        # crawler_process.terminate()
