from flask import Blueprint, request, session, jsonify, redirect
from flask_cas import login_required
from sqlalchemy.exc import IntegrityError
from app import db, cas
from app.user.models import User
from app.courier.controllers import requires_master
import re

mod_user = Blueprint('user', __name__, url_prefix='/api')
valid_phone = re.compile("^[0-9]{10}$")


@mod_user.route('/login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return jsonify(success=True, user=user.to_dict())

    return jsonify(success=False), 401


'''
@mod_user.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    user = User.query.filter(User.email == email).first()
    if user is None or not user.check_password(password):
        return jsonify(success=False, message="Invalid Credentials"), 400

    session['user_id'] = user.id

    return jsonify(success=True, user=user.to_dict())
'''

'''
@mod_user.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id')
    return jsonify(success=True)
'''


@mod_user.route('/register', methods=['POST'])
@login_required
def create_user():
    try:
        user_id = request.form['id']
        name = cas.attributes['cas:Name']
        roll = cas.attributes['cas:RollNo']
        email = cas.attributes['cas:E-Mail']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    if valid_phone.match(user_id) is None:
        return jsonify(success=False, message="Please enter a valid phone number"), 400

    u = User(user_id, name, email, roll)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="These credentials are already being used"), 400

    return jsonify(success=True)


@mod_user.route('/user', methods=['GET'])
@login_required
@requires_master
def get_all_users():
    users = User.query.all()
    return jsonify(success=True, users=[user.to_dict() for user in users])
