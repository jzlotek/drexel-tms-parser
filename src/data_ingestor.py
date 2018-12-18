from flask import Flask, request, Response
import db

app = Flask(__name__)


@app.route('/ingest', methods=['POST'])
def ingest():
    if request.json:
        print(request.json)
        # created
        return Response("", status=201)

    return Response("", status=400)


app.run(host="0.0.0.0", port=5001, debug=True)
