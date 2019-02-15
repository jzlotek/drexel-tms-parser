from flask import Flask, Response, request, render_template, send_from_directory
import os
from sdk.db import database
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
    query = database.get_query()

    # Drexel default to quarter
    if not request.args.get('isQuarter'):
        database.isQuarter(True, query)
    else:
        database.isQuarter(True, request.args.get('isQuarter'))

    database.query_builder(request.args, query)
    logger.info(request.args)
    data = database.execute(query)
    return json_response(data)


@app.route('/api/<q>', methods=['GET'])
def get_listing(q):
    query = database.get_query()
    data = database.get_list(q, query, request.args)
    return json_response(data)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 31536000
    if 'service-worker.js' in request.path:
        response.cache_control.max_age = 0

    return response

@app.route('/', methods=["GET"])
def get_home():
    # needs the index to be in the dist folder to work
    return send_from_directory('../dist', 'index.html')

@app.route('/static/<path:path>', methods=["GET"])
def get_file_static(path):
    # needs the index to be in the dist folder to work
    return send_from_directory('../dist/static', path)

@app.route('/<path:path>', methods=["GET"])
def get_file_non_static(path):
    # needs the index to be in the dist folder to work
    return send_from_directory('../dist', path)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 5000

    debug = False
    if os.environ.get('DEBUG'):
        debug = os.environ.get('DEBUG').lower() == 'true'
    try:
        app.run(host='0.0.0.0', port=PORT, debug=debug, threaded=True)
    except Exception as e:
        logger.error(e)
