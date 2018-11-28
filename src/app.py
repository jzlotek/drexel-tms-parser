from flask import Flask, render_template
import datetime
import multiprocessing
import os
from crawler.tms_crawler import Crawler


def run_crawler():
    try:
        crawler = Crawler()
        crawler.crawl()
    except Exception as e:
        print('\n\n{}\n\n{}\n\n'.format(str(e), str(datetime.datetime.now())))


app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("../dist/index.html")


@app.route('/output.json')
def get_output():
    return app.response_class(
        response="".join(open('./output.json', 'r').readlines()),
        mimetype='application/json'
    )


if __name__ == '__main__':

    if '.tmp' not in os.listdir('./'):
        os.mkdir('./.tmp')

    crawler_process = multiprocessing.Process(target=run_crawler)

    try:
        crawler_process.start()
        app.run(debug=True)
    except Exception as e:
        print(e)
        crawler_process.terminate()
