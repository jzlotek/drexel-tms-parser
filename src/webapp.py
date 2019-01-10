from flask import Flask, Response, request, render_template, send_from_directory
import os
from db import database
import json
from utils import logger

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")


def json_response(data):
    json_string = json.dumps(data)
    return Response(json_string, mimetype='application/json')


@app.route('/course', methods=['GET'])
def get_course():
    database.query_builder(request.args)
    logger.info(request.args)
    logger.info(database.get_query())
    data = database.execute()
    database.clear_query()
    return json_response(data)


@app.route('/api/<query>', methods=['GET'])
def get_listing(query):
    data = database.get_list(query, request.args)
    return json_response(data)


@app.route('/', methods=["GET"])
def get_home():
    # needs the index to be in the dist folder to work
    return render_template('index.html')

@app.route('/<path:path>', methods=['GET'])
def get_static(path):

    return send_from_directory('../dist', path)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 5000

    debug = False
    if os.environ.get('DEBUG'):
        debug = bool(os.environ.get('DEBUG'))
    try:
        app.run(host='0.0.0.0', port=PORT, debug=debug, threaded=(not debug))
    except Exception as e:
        logger.error(e)
