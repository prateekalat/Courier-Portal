from app import db
from datetime import datetime


class Courier(db.Model):
    __tablename__ = 'couriers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arrival_time = db.Column(db.String(30))
    contents = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Phone number of user
    user_name = db.Column(db.String(30))
    hostel = db.Column(db.String(30))
    room_no = db.Column(db.Integer)
    sender_address = db.Column(db.String(200))
    types = db.Column(db.String(100))
    received=db.Column(db.Boolean)

    user = db.relationship("User")

    def __init__(self, user_id, arrival_time, contents, hostel, room_no, types, sender_address, user_name="",received=False):
        # 'DD/MM/YYYY,HH:MM'
        #time = datetime.now()
        # arrival_time = str(time.day) + "/" + str(time.month) + "/" + str(time.year) + "," + str(time.hour) + ":" +
        # str(time.minute)
        #arrival_time = time.__format__("%a %d/%m/%Y %H:%M")
        self.arrival_time = arrival_time
        self.user_id = user_id
        self.contents = contents
        self.hostel = hostel
        self.room_no = room_no
        self.types = types
        self.sender_address = sender_address
        self.user_name = user_name
        self.received=received

    def to_dict(self):
        return {
            'id': self.id,
            'arrivalTime': self.arrival_time,
            'contents': self.contents,
            'user_name': self.user_name if self.user is None else self.user.name,
            'user_id': self.user_id,
            'hostel': self.hostel,
            'senderAddress': self.sender_address,
            'roomNo': self.room_no,
            'types': self.types,
            'received':self.received
        }

    def __repr__(self):
        return "Courier<%d> arrival_time: %s, contents: [%s], user_id: %d, hostel: %s, room_no: %d, types: %s, senders_address: %s user_name: %s received:%s" %  (
            self.id, self.arrival_time, self.contents, self.user_id, self.hostel, self.room_no, self.types, self.sender_address,self.user_name,self.received)
