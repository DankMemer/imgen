import asyncio
import json
import os
import threading
import traceback

import rethinkdb as r
from flask import Flask, render_template, request, g, jsonify

from dashboard import dash
from utils.db import get_db
from utils.ratelimits import ratelimit

# Initial require, the above line contains our endpoints.

config = json.load(open('config.json'))
endpoints = None

app = Flask(__name__, template_folder='views', static_folder='views/assets')
app.register_blueprint(dash)

app.config['SECRET_KEY'] = config['client_secret']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

if 'sentry_dsn' in config:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(config['sentry_dsn'],
                    integrations=[FlaskIntegration()])


@app.before_first_request
def init_app():
    def run_gc_forever(loop):
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        except (SystemExit, KeyboardInterrupt):
            loop.close()

    gc_loop = asyncio.new_event_loop()
    gc_thread = threading.Thread(target=run_gc_forever, args=(gc_loop,))
    gc_thread.start()
    g.gc_loop = gc_loop

    from utils.endpoint import endpoints as endpnts
    global endpoints
    endpoints = endpnts
    import endpoints as _  # noqa: F401


def require_authorization(func):
    def wrapper(*args, **kwargs):
        if r.table('keys').get(request.headers.get('authorization', '')).coerce_to('bool').default(False).run(get_db()):
            return func(*args, **kwargs)

        return jsonify({'status': 401, 'error': 'You are not authorized to access this endpoint'}), 401

    return wrapper


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'rdb'):
        g.rdb.close()


@app.route('/', methods=['GET'])
def index():
    data = {}

    for endpoint in endpoints:
        data[endpoint] = {'hits': endpoints[endpoint].hits,
                          'avg_gen_time': endpoints[endpoint].get_avg_gen_time()}

    return render_template('index.html', data=data)


@app.route('/endpoints.json', methods=['GET'])
def endpoints():
    return jsonify({"endpoints": [{'name': x, 'parameters': y.params} for x, y in endpoints.items()]})


@app.route('/documentation')
def docs():
    return render_template('docs.html', url=request.host_url, data=sorted(endpoints.items()))


@app.route('/api/<endpoint>', methods=['GET', 'POST'])
@require_authorization
@ratelimit
def api(endpoint):
    if endpoint not in endpoints:
        return jsonify({'status': 404, 'error': 'Endpoint {} not found!'.format(endpoint)}), 404
    if request.method == 'GET':
        text = request.args.get('text', '')
        avatars = [x for x in [request.args.get('avatar1', None), request.args.get('avatar2', None)] if x]
        usernames = [x for x in [request.args.get('username1', None), request.args.get('username2', None)] if x]
    else:
        if not request.is_json:
            return jsonify({'status': 400, 'message': 'when submitting a POST request you must provide data in the '
                                                      'json format'}), 400
        request_data = request.json
        text = request_data.get('text', '')
        avatars = list(request_data.get('avatars', []))
        usernames = list(request_data.get('usernames', []))
    try:
        result = endpoints[endpoint].run(key=request.headers.get('authorization'),
                                         text=text,
                                         avatars=avatars,
                                         usernames=usernames)
    except Exception as e:
        print(e, ''.join(traceback.format_tb(e.__traceback__)))
        return jsonify({'status': 500, 'error': str(e)}), 500
    return result, 200


if __name__ == '__main__':
    app.run()
