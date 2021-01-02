import json

from flask import Flask, Response

app = Flask(__name__)


@app.route('/')
def index():
    return Response('www.porta.com.mk')


@app.route('/<building>')
def data(building):
    try:
        with open(f'static/{building}.json') as building:
            response = Response(
                json.dumps(json.loads(building.read()), ensure_ascii=False),
                mimetype='application/json'
            )
            response.headers['Access-Control-Allow-Origin'] = '*'

            return response

    except Exception:

        return Response('Bad request', 400)


if __name__ == '__main__':

    app.run()
