# Import flask and template operators
import flask
from flask import Flask, render_template, session, jsonify, redirect
from flask_cas import CAS, login_required
from flask_mail import Mail,Message

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from functools import wraps

# Define the WSGI application object

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'himanshubhatia98@gmail.com',
    MAIL_PASSWORD = ''
    )
mail = Mail(app)

# Configurations
app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

cas = CAS(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 200


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message="Unauthorized", success=False), 401
        return f(*args, **kwargs)

    return decorated


# Import a module / component using its blueprint handler variable (mod_auth)
from app.user.controllers import mod_user
from app.courier.controllers import mod_courier

# Register blueprint(s)
app.register_blueprint(mod_user)
app.register_blueprint(mod_courier)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

from app.user.models import User


@app.route('/')
@login_required
def login():
    print(cas.username, cas.attributes)
    email = cas.attributes['cas:E-Mail']

    # if 'user_id' not in session:
    user = User.query.filter(User.email == email).first()
    # else:
    #     return redirect('/courier/list')

    if user is not None:
        print(user)
        session['user_id'] = user.id
        return redirect('/courier/list')
    else:
        return redirect('/register')
