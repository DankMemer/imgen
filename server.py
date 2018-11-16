import asyncio
import json
import os
import threading
import traceback

import rethinkdb as r
from flask import Flask, render_template, request, g, jsonify

from dashboard import dash
from utils.ratelimits import ratelimit
from utils.db import get_db

config = json.load(open('config.json'))

app = Flask(__name__, template_folder='views', static_folder='views/assets')
app.register_blueprint(dash)

app.config['SECRET_KEY'] = config['client_secret']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

endpoints = None


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

    import endpoints as endpnts
    global endpoints
    endpoints = endpnts


def require_authorization(func):
    def wrapper(*args, **kwargs):
        if r.table('keys').get(request.headers.get('authorization', '')).coerce_to('bool').default(False).run(get_db()):
            return func(*args, **kwargs)
        else:
            return jsonify({'status': 401, 'error': 'You are not authorized to access this endpoint'}), 401

    return wrapper


@app.route('/', methods=['GET'])
def index():
    data = {}

    for endpoint in endpoints.endpoints:
        data[endpoint] = {'hits': endpoints.endpoints[endpoint].hits,
                          'avg_gen_time': endpoints.endpoints[endpoint].get_avg_gen_time()}

    return render_template('index.html', data=data)


@app.route('/endpoints')
def api_endpoints():
    return render_template('endpoints.html', data=sorted(endpoints.endpoints.keys()))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/<endpoint>', methods=['GET'])
@require_authorization
@ratelimit
def api(endpoint):
    if endpoint not in endpoints.endpoints:
        return jsonify({'status': 404, 'error': 'Endpoint {} not found!'.format(endpoint)}), 404
    try:
        result = endpoints.endpoints[endpoint].run(key=request.headers.get('authorization'),
                                                   text=request.args.get('text', ''),
                                                   avatars=[request.args.get('avatar1', ''),
                                                            request.args.get('avatar2', '')],
                                                   usernames=[request.args.get('username1', ''),
                                                              request.args.get('username2', '')]
                                                   )
    except Exception as e:
        print(e, ''.join(traceback.format_tb(e.__traceback__)))
        result = jsonify({'status': 500, 'error': str(e)}), 500
    return result, 200


if __name__ == '__main__':
    app.run()
