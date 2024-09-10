from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from flask_jwt_extended import get_csrf_token,create_access_token, jwt_required, JWTManager, get_jwt_identity, set_access_cookies, unset_jwt_cookies
import db
from config.config import config
import logging

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_COOKIE_CSRF_PROTECT'] = config.JWT_COOKIE_CSRF_PROTECT
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Enable JWT in cookies
app.config['JWT_COOKIE_SECURE'] = False  # Disable secure cookies for local development
jwt = JWTManager(app)

# Run Flyway migrations at application start
db.run_db_schema_updates()


# Entry point (login)
@app.route('/', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']

        user = db.get_user_by_username(user_name)
        if user and user[2] == password:
            access_token = create_access_token(identity=user[1])
            response = make_response(redirect(url_for('button_page')))  # Redirect to button page
            set_access_cookies(response, access_token)  # Set JWT token in cookies
            return response
        else:
            return "Invalid credentials", 401
    return render_template('entry.html')


# Protected page with button
@app.route('/button', methods=['GET'])
@jwt_required()
def button_page():
    logging.info("CSRF Token: %s", request.cookies.get('csrf_access_token'))
    return render_template('button.html')


# Handle button click
@app.route('/click', methods=['POST'])
@jwt_required()
def handle_click():
    current_user = get_jwt_identity()
    db.log_click(current_user)
    return jsonify(message=f'Click logged for user {current_user}.')


if __name__ == '__main__':
    app.run(debug=True)
