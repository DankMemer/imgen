import sys
import traceback
from flask import Flask, jsonify, request

from endpoints import (gay, trigger, trash, disability, quote, abandon, ban, slap, bed, brain, tweet,  # noqa: F401
    ugly, spank, shit, hitler)  # noqa: F401
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
        result = endpoints[endpoint].generate(text=request.args.get('text', ''),
                                              avatars=[request.args.get('avatar1', ''), request.args.get('avatar2', '')],
                                              usernames=[request.args.get('username1', ''), request.args.get('username2', '')])
    except Exception as e:
        print(e, ''.join(traceback.format_tb(e.__traceback__)))
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
