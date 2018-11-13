from flask import render_template, request, Blueprint, url_for, session, redirect
import json
from utils.make_session import make_session
import rethinkdb as r
import hashlib
from random import randint

config = json.load(open('config.json'))

dash = Blueprint('dashboard', __name__, template_folder='views', static_folder='views/assets')

API_BASE_URL = 'https://discordapp.com/api'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'
RDB_ADDRESS = config['rdb_address']
RDB_PORT = config['rdb_port']
RDB_DB = config['rdb_db']

rdb = r.connect(RDB_ADDRESS, RDB_PORT, db=RDB_DB)


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
    keys = r.table('keys').filter(r.row['owner'] == user['id']).run(rdb)
    return render_template('dashboard.html', name=user['username'], keys=keys)


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
        }).run(rdb)
        result = 'Application Submitted 👌'
        return render_template('result.html', result=result, success=True)


@dash.route('/admin')
def admin():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    apps = r.table('applications').run(rdb)
    keys = r.table('keys').run(rdb)
    return render_template('admin.html', name=user['username'],  apps=apps, keys=keys)


@dash.route('/approve/<key_id>')
def approve(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    key = r.table('applications').get(key_id).run(rdb)
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
        "unlimited": False
    }).run(rdb)
    r.table('applications').get(key_id).delete().run(rdb)
    return redirect(url_for('.admin'))


@dash.route('/decline/<key_id>')
def decline(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    r.table('applications').get(key_id).delete().run(rdb)
    return redirect(url_for('.admin'))


@dash.route('/delete/<key_id>')
def delete(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    r.table('keys').get(key_id).delete().run(rdb)
    return redirect(url_for('.admin'))


@dash.route('/unlimited/<key_id>')
def unlimited(key_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    if 'id' not in user:
        return redirect(url_for('.login'))
    if user['id'] not in config['admins']:
        return render_template('gitout.html')
    key = r.table('keys').get(key_id).run(rdb)
    if key['unlimited']:
        r.table('keys').get(key_id).update({"unlimited": False}).run(rdb)
    else:
        r.table('keys').get(key_id).update({"unlimited": True}).run(rdb)
    return redirect(url_for('.admin'))
