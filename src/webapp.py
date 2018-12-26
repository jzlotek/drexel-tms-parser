from flask import Flask, Response, request, render_template
import os
from db import database
import json
from utils import logger

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")


@app.route('/course', methods=['GET'])
def get_course():
    database.query_builder(request.args)

    return Response(json.dumps(database.execute()), mimetype='application/json')

@app.route('/', methods=["GET"])
def get_home():
    # needs the index to be in the dist folder to work
    return render_template('index.html')


if __name__ == '__main__':
    PORT = int(os.environ['PORT']) if os.environ['PORT'] else 5000

    if 'dist' not in os.listdir('../'):
        logger.debug("Making dist folders")
        os.mkdir('../dist')

    if '.tmp' not in os.listdir('../dist'):
        os.mkdir('../dist/.tmp')

    debug = False
    if os.environ.get('DEBUG'):
        debug = bool(os.environ.get('DEBUG'))
    try:
        app.run(port=PORT, debug=debug, threaded=(not debug))
    except Exception as e:
        logger.error(e)
