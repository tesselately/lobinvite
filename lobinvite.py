# -*- coding: utf-8 -*-
from datetime import datetime
import os
from random import choice
import string

from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flask_openid import OpenID
import psycopg2


app = Flask(__name__)

app.config.update(
    DSN='dbname=lobsters',
    #DSN='dbname=lobsters user=lobsters host=localhost',
    SECRET_KEY='development key',
    DEBUG=True,
    FRIEND_STEAM_IDS=(),
    INVITE_CODES=(),
)

if 'LOBINVITE_SETTINGS' in os.environ:
    app.config.from_envvar('LOBINVITE_SETTINGS')


oid = OpenID(app)


@app.route('/join', methods=['GET', 'POST'])
@oid.loginhandler
def index():
    if request.method == 'POST':
        return oid.try_login('http://steamcommunity.com/openid')
    if request.args.get('code') in app.config['INVITE_CODES']:
        return invite('invite code ' + request.args['code'])
    return render_template('index.html')


@oid.after_login
def finish_steam_login(resp):
    steam_id = resp.identity_url.split('/')[-1]
    if steam_id in app.config['FRIEND_STEAM_IDS']:
        return invite("steam " + steam_id)
    return render_template('ask.html')


def invite(reason):
    now = datetime.utcnow().isoformat()
    letter_digits = string.letters + string.digits
    code = ''.join(choice(letter_digits) for x in xrange(15))

    # Add it to the database.
    conn = psycopg2.connect(app.config['DSN'])
    cur = conn.cursor()
    cur.execute("INSERT INTO invitations (user_id, code, created_at, updated_at, memo) VALUES (%s, %s, %s, %s, %s)",
        (1, code, now, now, 'self-serve invitation (%s)' % reason))
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/invitations/' + code)


if __name__ == '__main__':
    app.run()
