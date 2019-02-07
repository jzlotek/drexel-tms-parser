from flask import Flask, request, Response
from sdk.db.db_functions import import_to_db, import_to_db_bulk, import_to_db_single
from utils import logger
import os
import json

app = Flask(__name__)


@app.route('/ingest', methods=['POST'])
def ingest():
    logger.info(request)
    mode = request.args.get('mode')
    if request.json:
        # created
        if not mode:
            import_to_db_bulk(request.json.get('data'), request.json.get('name'))
        elif mode == 'single':
            body = request.json
            import_to_db_single(body.get('college_name'), body.get('data'), body.get('name'))
        else:
            return Response('{"status": 401, "reason": "unknown ingest mode: {mode}"}'.format(mode=mode), status=401, mimetype="application/json")

        return Response("", status=201)

    return Response("", status=400)

if __name__ == "__main__":
    PORT = int(os.environ['PORT']) if os.environ.get('PORT') else 5001

    app.run(host="0.0.0.0", port=PORT, debug=True, threaded=False)
