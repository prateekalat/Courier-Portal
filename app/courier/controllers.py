from functools import wraps
import re

from flask import Blueprint, request, session, jsonify, redirect
from flask_cas import login_required
from app import db,mail,cas
from app.courier.models import Courier
from app.user.models import User
from flask_mail import Mail,Message

mod_courier = Blueprint('courier', __name__, url_prefix='/api')

phone_regex = re.compile('^[0-9]{10}$')

def requires_master(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        if user is not None and user.master:
            return f(*args, **kwargs)
        else:
            return jsonify(message="Unauthorized", success=False), 401

    return decorated


@mod_courier.route('/courier', methods=['POST'])
@login_required
@requires_master
def create_courier():

    empty_fields = []

    user_name = request.form['user_name']
    arrival_time=request.form['arrivalTime']
    contents = request.form['contents']
    user_id = request.form['user_id']
    hostel = request.form['hostel']
    roomNo = request.form['roomNo']
    sender_address = request.form['sender_address']
    types = request.form['types']

    if phone_regex.match(user_id) is None:
        # return jsonify(success=False, field="user_id")
        empty_fields.append('user_id')

    if user_name is "":
        # return jsonify(success=False, field="user_name")
        empty_fields.append('user_name')

    if contents is "":
        empty_fields.append('contents')

    if hostel is "":
        empty_fields.append('hostel')

    if roomNo is "":
        empty_fields.append('roomNo')

    if sender_address is "":
        empty_fields.append('sender_address')

    if types is "":
        empty_fields.append('types')

    if len(empty_fields) > 0:
        print(empty_fields)
        return jsonify(success=False, fields=empty_fields)


    # user = User.query.filter(User.id == user_id).first()
    # if user is None:
    #     return jsonify(success=False)

    courier = Courier(user_id,arrival_time, contents, hostel, roomNo, types, sender_address, user_name)
    db.session.add(courier)
    db.session.commit()
    print(courier.user)

    try:
        # courierslist=Courier.query.all()
        # print(courierslist)
        msg = Message("Hello!",
          sender="himanshubhatia98@gmail.com",
          # recipients=[courierslist[len(courierslist)-1].user.email])
          recipients=[courier.user.email])
        msg.body = "This mail is to inform you that a courier has arrived for you from "+sender_address+" of type "+ types +" having contents as "+contents+"."            
        mail.send(msg)
        # return redirect('/courier/list')
    except:
        pass

    finally:
        return jsonify(success=True, courier=courier.to_dict())


@mod_courier.route('/courier', methods=['GET'])
@login_required
def get_all_couriers():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    if user.master is True:
        couriers = Courier.query.all()
    else:
        couriers = Courier.query.filter(Courier.user_id == user_id).all()
    return jsonify(success=True, couriers=[courier.to_dict() for courier in couriers], user=user.to_dict())


@mod_courier.route('/courier/anonymous', methods=['GET'])
@login_required
def get_anonymous_couriers():
    couriers = Courier.query.outerjoin(User).filter(User.id == None).all()
    return jsonify(success=True, couriers=[courier.to_dict() for courier in couriers])


@mod_courier.route('/courier/<id>', methods=['GET'])
@login_required
def get_courier(id):
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    if (user.master is not True):
        courier = Courier.query.filter(Courier.id == id, Courier.user_id == user_id).first()
    else:
        courier = Courier.query.filter(Courier.id == id ).first()
    if courier is None:
        return jsonify(success=False), 404
    else:
        return jsonify(success=True, courier=courier.to_dict())


@mod_courier.route('/courier/<id>', methods=['POST'])
@login_required
@requires_master
def edit_courier(id):
    user_id = session['user_id']
    courier = Courier.query.filter(Courier.id == id, Courier.user_id == user_id).first()
    if courier is None:
        return jsonify(success=False), 404
    else:
        courier.user_id = request.form['user_id']
        courier.contents = request.form['contents']
        courier.hostel = request.form['hostel']
        courier.roomNo = request.form['roomNo']
        courier.types = request.form['types']
        db.session.commit()
        return jsonify(success=True)


@mod_courier.route('/courier/<id>/delete', methods=['POST'])
@login_required
@requires_master
def delete_courier(id):
    courier = Courier.query.filter(Courier.id == id).first()
    if courier is None:
        return jsonify(success=False), 404
    else:
        db.session.delete(courier)
        db.session.commit()
        return jsonify(success=True)

@mod_courier.route('/courier/received', methods=['POST'])
@login_required
@requires_master
def received():
    courier = Courier.query.all()
    for i in courier:
        break
    db.session.commit()
    return jsonify(success=True)

@mod_courier.route('/courier/search/<query>', methods=['GET'])
@login_required
@requires_master
def search_courier(query):
    # users = User.query.filter(User.name.like('%' + query + '%')).all()
    # couriers = []
    # for user in users:
    #     couriers += Courier.query.filter(Courier.user_id == user.id).all()
    couriers = Courier.query.filter(Courier.user_name.like('%' + query + '%'))
    return jsonify(success=True, couriers=[courier.to_dict() for courier in couriers])

@mod_courier.route('/courier/received', methods=['GET'])
@login_required
@requires_master
def showReceived():
    couriers = Courier.query.filter(Courier.received == True).all()
    return jsonify(success=True, couriers=[courier.to_dict() for courier in couriers])

@mod_courier.route('/courier/notReceived', methods=['GET'])
@login_required
@requires_master
def showNotReceived():
    couriers = Courier.query.filter(Courier.received == False).all()
    return jsonify(success=True, couriers=[courier.to_dict() for courier in couriers])

@mod_courier.route('/courier/modify/<id>', methods=['POST'])
@login_required
@requires_master
def modify(id):
    print(request.form['arrivalTime'])
    courier = Courier.query.filter(Courier.id == id).first()
    courier.user_name = request.form['user_name']
    courier.user_id = request.form['user_id']
    courier.contents = request.form['contents']
    courier.hostel = request.form['hostel']
    courier.roomNo = request.form['roomNo']
    courier.types = request.form['types']
    courier.arrival_time = request.form['arrivalTime']
    db.session.commit()
    return jsonify(success=True)


@mod_courier.route('/courier/subReceived', methods=['POST'])
@login_required
@requires_master
def subRec():
    ids=request.form.getlist('ids[]')
    print(ids)
    for i in ids:
       courier = Courier.query.filter(Courier.id == i).first()
       courier.received = True
       db.session.commit()
    return jsonify(sucess=True)
