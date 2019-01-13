from flask import Flask, request, Response
from sdk.db.db_functions import import_to_db
from utils import logger
import os

app = Flask(__name__)


@app.route('/ingest', methods=['POST'])
def ingest():
    logger.info(request)
    if request.json:
        # created
        import_to_db(request.json.get('data'), request.json.get('name'))

        return Response("", status=201)

    return Response("", status=400)

PORT = int(os.environ['PORT']) if os.environ['PORT'] else 5001

app.run(host="0.0.0.0", port=PORT, debug=True, threaded=True)
