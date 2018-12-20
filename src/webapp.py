from flask import Flask, Response, request
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


if __name__ == '__main__':
    if 'dist' not in os.listdir('../'):
        logger.debug("Making dist folders")
        os.mkdir('../dist')

    if '.tmp' not in os.listdir('../dist'):
        os.mkdir('../dist/.tmp')

    debug = False
    if os.environ.get('DEBUG'):
        debug = bool(os.environ.get('DEBUG'))
    try:
        app.run(host="0.0.0.0", debug=debug, threaded=(not debug))
    except Exception as e:
        print(e)
