try:
    import ujson as json
except ImportError:
    import json

from flask import session
from requests_oauthlib import OAuth2Session

config = json.load(open('config.json'))

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
API_BASE_URL = 'https://discordapp.com/api/'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'


def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None, redirect_uri=None):
    return OAuth2Session(
        client_id=CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=redirect_uri,
        auto_refresh_kwargs={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL, token_updater=token_updater)
