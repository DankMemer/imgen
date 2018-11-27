import hashlib
import json
from random import randint

import rethinkdb as r
from flask import render_template, request, Blueprint, url_for, session, redirect

from utils.db import get_db
from utils.make_session import make_session

config = json.load(open('config.json'))

dash = Blueprint('dashboard', __name__, template_folder='views', static_folder='views/assets')

API_BASE_URL = 'https://discordapp.com/api'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'


@dash.route('/login')
def login():
    discord = make_session(scope='identify email', redirect_uri=request.host_url + 'callback')
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    return redirect(authorization_url)


@dash.route('/logout')
def logout():
    session.clear()
    return redirect(request.host_url)


@dash.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'), redirect_uri=request.host_url + 'callback')
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=config['client_secret'],
        authorization_response=request.url)
    session['oauth2_token'] = token
    return redirect(url_for('.dashboard'))


@dash.route('/dashboard')
def dashboard():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    is_admin = user['id'] in config['admins']
    keys = r.table('keys').filter(r.row['owner'] == user['id']).run(get_db())
    return render_template('dashboard.html', name=user['username'], keys=keys, admin=is_admin)


@dash.route('/request', methods=['GET', 'POST'])
def request_key():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if request.method == 'GET':
        return render_template('request.html')
    elif request.method == 'POST':
        name = request.form.get('name', None)
        reason = request.form.get('reason', None)
        if not reason or not name:
            result = 'Please enter a name and reason for your application'
            return render_template('result.html', result=result, success=False)
        r.table('applications').insert({
            "owner": user['id'],
            "email": user['email'],
            "name": name,
            "owner_name": f'{user["username"]}#{user["discriminator"]}',
            "reason": reason
        }).run(get_db())
        result = 'Application Submitted 👌'
        return render_template('result.html', result=result, success=True)


@dash.route('/createkey', methods=['GET', 'POST'])
def create_key():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        name = request.form.get('name', None)
        token = request.form.get('token', None)
        owner = request.form.get('owner', None)
        owner_name = request.form.get('owner_name', None)
        email = request.form.get('email', None)
        if not token or not name or not owner or not owner_name or not email:
            result = 'Please fill in all required inputs'
            return render_template('result.html', result=result, success=False)
        r.table('keys').insert({
            "id": token,
            "name": name,
            "owner": owner,
            "owner_name": owner_name,
            "email": email,
            "total_usage": 0,
            "usages": {},
            "unlimited": False,
            "ratelimit_reached": 0
        }).run(get_db())
        result = 'Key Created 👌'
        return render_template('result.html', result=result, success=True)


@dash.route('/admin')
def admin():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    apps = r.table('applications').run(get_db())
    keys = r.table('keys').run(get_db())
    return render_template('admin.html', name=user['username'], apps=apps, keys=keys)


@dash.route('/approve/<key_id>')
def approve(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    key = r.table('applications').get(key_id).run(get_db())
    m = hashlib.sha256()
    m.update(key['id'].encode())
    m.update(str(randint(10000, 99999)).encode())
    token = m.hexdigest()
    r.table('keys').insert({
        "id": token,
        "name": key['name'],
        "owner": key['owner'],
        "owner_name": key['owner_name'],
        "email": key['email'],
        "total_usage": 0,
        "usages": {},
        "unlimited": False,
        "ratelimit_reached": 0
    }).run(get_db())
    r.table('applications').get(key_id).delete().run(get_db())
    return redirect(url_for('.admin'))


@dash.route('/decline/<key_id>')
def decline(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    r.table('applications').get(key_id).delete().run(get_db())
    return redirect(url_for('.admin'))


@dash.route('/delete/<key_id>')
def delete(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    r.table('keys').get(key_id).delete().run(get_db())
    return redirect(url_for('.admin'))


@dash.route('/unlimited/<key_id>')
def unlimited(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    key = r.table('keys').get(key_id).run(get_db())
    if key['unlimited']:
        r.table('keys').get(key_id).update({"unlimited": False}).run(get_db())
    else:
        r.table('keys').get(key_id).update({"unlimited": True}).run(get_db())
    return redirect(url_for('.admin'))
