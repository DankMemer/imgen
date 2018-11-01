import json
import traceback

from flask import Flask, abort, jsonify, render_template, request

import endpoints

app = Flask(__name__, template_folder='views', static_folder='views/assets')


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
        if request.headers.get('authorization', None) in get_auth_keys():
            return func(*args, **kwargs)
        else:
            abort(jsonify({'status': 401, 'error': 'You are not authorized to access this endpoint'}))

    return wrapper


@app.route('/', methods=['GET'])
def index():
    data = {}

    for endpoint in endpoints.endpoints:
        data[endpoint] = {'hits': endpoints.endpoints[endpoint].hits, 'avg_gen_time': endpoints.endpoints[endpoint].get_avg_gen_time()}

    return render_template('index.html', data=data)


@app.route('/endpoints')
def api_endpoints():
    return render_template('endpoints.html', data=sorted(endpoints.endpoints.keys()))


@app.route('/api/<endpoint>', methods=['GET'])
@require_authorization
def api(endpoint):
    if endpoint not in endpoints.endpoints:
        return jsonify({'status': 404, 'error': 'Endpoint {} not found!'.format(endpoint)})

    try:
        result = endpoints.endpoints[endpoint].run(text=request.args.get('text', ''),
                                                   avatars=[request.args.get('avatar1', ''), request.args.get('avatar2', '')],
                                                   usernames=[request.args.get('username1', ''), request.args.get('username2', '')])
    except Exception as e:
        print(e, ''.join(traceback.format_tb(e.__traceback__)))
        result = jsonify({'status': 500, 'error': str(e)})
    return result


if __name__ == '__main__':
    app.run()
