import json
import traceback
import os
import rethinkdb as r

from flask import Flask, jsonify, render_template, request, make_response

import endpoints
from utils.ratelimits import ratelimit

from dashboard import dash

config = json.load(open('config.json'))

RDB_ADDRESS = config['rdb_address']
RDB_PORT = config['rdb_port']
RDB_DB = config['rdb_db']

rdb = r.connect(RDB_ADDRESS, RDB_PORT, db=RDB_DB)

app = Flask(__name__, template_folder='views', static_folder='views/assets')
app.register_blueprint(dash)

app.config['SECRET_KEY'] = config['client_secret']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


def require_authorization(func):
    def wrapper(*args, **kwargs):
        if r.table('keys').get(request.headers.get('authorization', '')).coerce_to('bool').default(False).run(rdb):
            return func(*args, **kwargs)
        else:
            return make_response((jsonify({'status': 401,
                                           'error': 'You are not authorized to access this endpoint'}),
                                  401))
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
        return make_response((
            jsonify({'status': 404, 'error': 'Endpoint {} not found!'.format(endpoint)}), 404))
        # TODO: Figure out why setting status code here does not work and always returns 200

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
        result = make_response((jsonify({'status': 500,
                                         'error': str(e)}), 500))
        # TODO: Figure out why setting status code here does not work and always returns 200
    return result


if __name__ == '__main__':
    app.run()
