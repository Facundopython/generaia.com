from flask import Flask, redirect, url_for, session, render_template
from flask_oauthlib.client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv("GOOGLE_CLIENT_ID"),
    consumer_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    request_token_params={'scope': 'email profile'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Acceso denegado'
    session['google_token'] = (response['access_token'], '')
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run()
