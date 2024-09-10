from flask import Flask, jsonify, render_template, redirect, url_for, request, session
from authlib.integrations.flask_client import OAuth
from config.config import config
import db

app = Flask(__name__)
app.secret_key = config.JWT_SECRET_KEY

# Initialize OAuth
oauth = OAuth(app)
keycloak = oauth.register(
    name='keycloak',
    client_id=config.KEYCLOAK_CLIENT_ID,
    client_secret=config.KEYCLOAK_CLIENT_SECRET,
    server_metadata_url=f"{config.KEYCLOAK_SERVER}/realms/{config.KEYCLOAK_REALM}/.well-known/openid-configuration",
    client_kwargs={
        'scope': 'openid profile email',
    }
)

@app.route('/')
def home():
    return 'Welcome to the Flask application'

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return keycloak.authorize_redirect(redirect_uri=redirect_uri)

@app.route('/auth')
def auth():
    token = keycloak.authorize_access_token()
    session['user'] = token['userinfo']['given_name']
    return redirect('/button')

@app.route('/button')
def button_page():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('button.html')

@app.route('/click', methods=['POST'])
def handle_click():
    db.log_click(session.get('user'))
    return jsonify(message=f'Click logged for user {session.get("user")}.')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
