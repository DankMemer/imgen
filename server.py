import json
import sys
import traceback

from flask import Flask, abort, jsonify, render_template, request

from utils.endpoint import Endpoint

from endpoints import (abandon, ban, bed, brain,  # noqa: F401; noqa: F401
                       byemom, disability, facts, gay, hitler, invert, jail,
                       quote, shit, slap, spank, trash, trigger, tweet, ugly,
                       warp, whodidthis)

app = Flask(__name__)
endpoints = {}


def get_auth_keys():
    try:
        with open('keys.json') as keys:
            data = json.load(keys)
            if not isinstance(data, list):
                print('keys.json must only contain an array of valid auth tokens')
                return []
            else:
                return data
    except FileNotFoundError:
        print('keys.json wasn\'t found in the current directory')
        return []


def require_authorization(func):
    def wrapper(*args, **kwargs):
        print('running')
        if request.headers.get('authorization', None) in get_auth_keys():
            return func(*args, **kwargs)
        else:
            abort(jsonify({'status': 401, 'error': 'You are not authorized to access this endpoint'}))

    return wrapper


@app.route('/', methods=['GET'])
def index():
    return 'hi'


@app.route('/api/<endpoint>', methods=['GET'])
@require_authorization
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
