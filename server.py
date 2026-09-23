import asyncio

try:
    import ujson as json
except ImportError:
    import json

import os
import threading
import traceback
from functools import lru_cache

import rethinkdb as r
from flask import Flask, render_template, request, g, jsonify, make_response, send_file

from dashboard import dash
from utils.db import get_db, get_redis
from utils.ratelimits import ratelimit, endpoint_ratelimit
from utils.exceptions import BadRequest
from utils.http import MAX_FILE_SIZE

from sentry_sdk import capture_exception

# Initial require, the above line contains our endpoints.

config = json.load(open('config.json'))
endpoints = None

JPEG_ENDPOINTS = set('abandon aborted affect armor balloon boo brain changemymind cheating citation confusedcat cry doglemon emergencymeeting excuseme expandingwwe facts farmer fuck godwhy goggles humansgood inator justpretending keepurdistance knowyourlocation lick master note nothing obama ohno piccolo plan presentation savehumanity shit slapsroof sneakyfox stroke surprised sword theoffice thesearch violence violentsparks vr walking'.split())
GIF_ENDPOINTS = set('airpods america communism dank kowalski salty trigger'.split())
VIDEO_ENDPOINTS = set('crab letmein'.split())
PREVIEW_EXTENSIONS = ('bmp', 'png', 'jpg', 'jpeg', 'webp', 'gif')
PREVIEW_OVERRIDES = {'profile': 'assets/profile/background.jpg', 'tweet': 'assets/tweet/trump.bmp', 'thesearch': 'assets/search/thesearch.bmp', 'savehumanity': 'assets/humanity/humanity.bmp'}
TEXT_LABELS = {
    'balloon': ('Balloon text', 'Label text'),
    'boo': ('First caption', 'Second caption'),
    'brain': ('First panel', 'Second panel', 'Third panel', 'Fourth panel'),
    'cheating': ('Your message', 'Classmate message'),
    'citation': ('Heading', 'Details', 'Penalty'),
    'confusedcat': ('Left caption', 'Right caption'),
    'crab': ('Top line', 'Bottom line'),
    'doglemon': ('Lemon text', 'Dog text'),
    'expandingwwe': ('First panel', 'Second panel', 'Third panel', 'Fourth panel', 'Fifth panel'),
    'farmer': ('Cloud text', 'Farmer text'),
    'fuck': ('Left caption', 'Right caption'),
    'justpretending': ('Top caption', 'Repeated caption'),
    'knowyourlocation': ('Top text', 'Bottom text'),
    'lick': ('First caption', 'Second caption'),
    'master': ('First caption', 'Second caption', 'Third caption'),
    'plan': ('First panel', 'Second panel', 'Third panel'),
    'sneakyfox': ('Fox text', 'Other text'),
    'surprised': ('Me text', 'Also me text'),
    'sword': ('Sword text', 'Food text'),
    'theoffice': ('Left caption', 'Right caption'),
    'violentsparks': ('Person text', 'Sparks text'),
}
PARAMETER_DESCRIPTIONS = {
    'avatar0': 'Image URL for the first image.',
    'avatar1': 'Image URL for the second image.',
    'username0': 'First display name.',
    'username1': 'Second display name. Optional for tweet; sets the handle.',
    'text': 'Text to render.',
    'top_text': 'Top caption. Defaults to TOP TEXT.',
    'bottom_text': 'Bottom caption. Defaults to BOTTOM TEXT.',
    'color': 'Color name or hex value. Sets meme text or the profile level bar.',
    'font': 'Meme font name.',
    'altstyle': 'String true or false. True places text above the image. Defaults to false.',
    'bio': 'Profile bio. Text over 40 characters is shortened.',
    'title': 'Profile title.',
    'xp': 'Cumulative XP as decimal text. The profile level is XP divided by 100.',
    'bank': 'Bank balance as decimal text.',
    'wallet': 'Wallet balance as decimal text.',
    'inventory': 'Inventory summary text.',
    'prestige': 'Badge name from prestige1 through prestige10.',
    'active_effects': 'Effects separated by hyphens, each formatted as :item:name.',
    'command': 'Favorite command text.',
    'streak': 'Daily streak text.',
    'multiplier': 'Multiplier percentage text.',
}
ENDPOINT_NOTES = {
    'corporate': 'avatar2 is optional. If omitted, avatar1 is used twice.',
    'emergencymeeting': 'Text at or above 140 characters is shortened.',
    'expanddong': 'Only the first 500 characters are rendered.',
    'godwhy': 'Text at or above 127 characters is shortened.',
    'keepurdistance': 'Text at or above 30 characters is shortened.',
    'meme': 'Fonts: arial, arimobold, impact, robotomedium, robotoregular, sans, segoeuireg, tahoma, verdana. Standard style defaults to Impact and white. Alternate style uses text above the image, defaults to Arial and black, and ignores bottom_text.',
    'profile': 'Use a valid profile badge name for prestige. Supported active-effect items: alcohol, cupidsbigtoe, fakeid, padlock, sand, santashat, spinner, tidepod, landmine.',
    'nothing': 'Only the first 120 characters are rendered.',
    'piccolo': 'Only the first 300 characters are rendered.',
    'tweet': 'username2 sets the handle. If omitted, username1 is used.',
    'letmein': 'Text at or above 400 characters is shortened.',
    'yomomma': 'Returns a JSON object with a text field.',
}


def public_parameter(param):
    return {'avatar0': 'avatar1', 'avatar1': 'avatar2',
            'username0': 'username1', 'username1': 'username2'}.get(param, param)


@lru_cache(maxsize=256)
def preview_path(endpoint):
    if endpoint not in endpoints:
        return None
    if endpoint in PREVIEW_OVERRIDES:
        path = PREVIEW_OVERRIDES[endpoint]
        return path if os.path.isfile(path) else None
    for extension in PREVIEW_EXTENSIONS:
        path = 'assets/{0}/{0}.{1}'.format(endpoint, extension)
        if os.path.isfile(path):
            return path
    return None


def output_type(endpoint):
    if endpoint == 'yomomma':
        return 'application/json'
    if endpoint in VIDEO_ENDPOINTS:
        return 'video/mp4'
    if endpoint in GIF_ENDPOINTS:
        return 'image/gif'
    if endpoint in JPEG_ENDPOINTS:
        return 'image/jpeg'
    return 'image/png'

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


@app.route('/')
def index():
    return render_template('index.html', active_home="nav-active")


@app.route('/stats', methods=['GET'])
def stats():
    data = {}

    for endpoint in endpoints:
        data[endpoint] = {'hits': get_redis().get(endpoint + ':hits') or 0,
                          'avg_gen_time': endpoints[endpoint].get_avg_gen_time()}

    return render_template('stats.html', data=data, active_stats="nav-active")


@app.route('/endpoints.json', methods=['GET'])
def endpoints():
    return jsonify({"endpoints": [{'name': x, 'parameters': [public_parameter(p) for p in y.params],
                                   'ratelimit': f'{y.rate}/{y.per}s'} for x, y in endpoints.items()]})


@app.route('/documentation')
def docs():
    data = sorted(endpoints.items())
    previews = {name: preview_path(name) for name, _ in data}
    text_labels = {name: {'text{}'.format(i + 1): label for i, label in enumerate(labels)}
                   for name, labels in TEXT_LABELS.items()}
    return render_template('docs.html', data=data, previews=previews,
                           output_type=output_type, text_labels=text_labels,
                           public_parameter=public_parameter,
                           parameter_descriptions=PARAMETER_DESCRIPTIONS, endpoint_notes=ENDPOINT_NOTES,
                           max_file_size=MAX_FILE_SIZE, active_docs="nav-active")


@app.route('/templates/<endpoint>')
def template_example(endpoint):
    path = preview_path(endpoint)
    if not path:
        return jsonify({'status': 404, 'error': 'Template not found'}), 404
    return send_file(path)


@app.route('/api/<endpoint>', methods=['GET', 'POST'])
@require_authorization
@ratelimit
def api(endpoint):
    if endpoint not in endpoints:
        return jsonify({'status': 404, 'error': 'Endpoint {} not found!'.format(endpoint)}), 404
    if request.method == 'GET':
        text = request.args.get('text', '')
        avatars = [x for x in [request.args.get('avatar1', request.args.get('image', None)),
                               request.args.get('avatar2', None)] if x]
        usernames = [x for x in [request.args.get('username1', None), request.args.get('username2', None)] if x]
        kwargs = {}
        for arg in request.args:
            if arg not in ['text', 'username1', 'username2', 'avatar1', 'avatar2']:
                kwargs[arg] = request.args.get(arg)
    else:
        if not request.is_json:
            return jsonify({'status': 400, 'message': 'when submitting a POST request you must provide data in the '
                                                      'JSON format'}), 400
        request_data = request.json
        text = request_data.get('text', '')
        avatars = list(request_data.get('avatars', list(request_data.get('images', []))))
        usernames = list(request_data.get('usernames', []))
        kwargs = {}
        for arg in request_data:
            if arg not in ['text', 'avatars', 'usernames']:
                kwargs[arg] = request_data.get(arg)
    cache = endpoints[endpoint].bucket
    max_usage = endpoints[endpoint].rate
    e_r = endpoint_ratelimit(auth=request.headers.get('Authorization', None), cache=cache, max_usage=max_usage)
    if e_r['X-RateLimit-Remaining'] == -1:
        x = make_response((jsonify({'status': 429, 'error': 'You are being ratelimited'}), 429,
                          {'X-RateLimit-Limit': e_r['X-RateLimit-Limit'],
                           'X-RateLimit-Remaining': 0,
                           'X-RateLimit-Reset': e_r['X-RateLimit-Reset'],
                           'Retry-After': e_r['Retry-After']}))
        return x
    try:
        result = endpoints[endpoint].run(key=request.headers.get('authorization'),
                                         text=text,
                                         avatars=avatars,
                                         usernames=usernames,
                                         kwargs=kwargs)
    except BadRequest as br:
        traceback.print_exc()
        if 'sentry_dsn' in config:
            capture_exception(br)
        return jsonify({'status': 400, 'error': str(br)}), 400
    except IndexError as e:
        traceback.print_exc()
        if 'sentry_dsn' in config:
            capture_exception(e)
        return jsonify({'status': 400, 'error': str(e) + '. Are you missing a parameter?'}), 400
    except Exception as e:
        traceback.print_exc()
        if 'sentry_dsn' in config:
            capture_exception(e)
        return jsonify({'status': 500, 'error': str(e)}), 500

    result.headers.add('X-RateLimit-Limit', max_usage)
    result.headers.add('X-RateLimit-Remaining', e_r['X-RateLimit-Remaining'])
    result.headers.add('X-RateLimit-Reset', e_r['X-RateLimit-Reset'])
    return result, 200


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
