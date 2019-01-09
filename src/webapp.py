from flask import Flask, Response, request, render_template, send_from_directory
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
    logger.info(request.args)
    logger.info(database.get_query())
    data = json.dumps(database.execute())
    database.clear_query()
    return Response(data, mimetype='application/json')


@app.route('/api/<query>', methods=['GET'])
def get_listing(query):

    return Response(json.dumps(database.get_list(query, request.args)), mimetype='application/json')


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
        debug = (os.environ.get('DEBUG').lower() == 'true')
    try:
        app.run(port=PORT, debug=debug, threaded=(not debug))
    except Exception as e:
        logger.error(e)
