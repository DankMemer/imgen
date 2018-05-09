import sys

from flask import Flask, jsonify, request

from endpoints import gay, trigger  # noqa: F401 F403
from utils.endpoint import Endpoint

app = Flask(__name__)
endpoints = {}


@app.route('/', methods=['GET'])
def index():
    return 'hi'


@app.route('/api/<endpoint>', methods=['GET'])
def api(endpoint):
    if endpoint not in endpoints:
        return jsonify({'status': 404, 'error': f'Endpoint {endpoint} not found!'})

    try:
        result = endpoints[endpoint].generate(request.headers.get('data-src'))
    except Exception as e:
        result = jsonify({'status': 500, 'error': str(e)})
    return result


if __name__ == "__main__":
    for e in filter(lambda module: str(module).startswith('endpoints.'), sys.modules):
        endpoint = sys.modules[e].setup()

        if not isinstance(endpoint, Endpoint):
            print(f'{endpoint} is not a valid endpoint!')
            continue

        endpoints.update({endpoint.name: endpoint})

    app.run(host='127.0.0.1', debug=True)
