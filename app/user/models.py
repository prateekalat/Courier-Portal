from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    roll = db.Column(db.Integer, unique=True)
    master = db.Column(db.Boolean)

    couriers = db.relationship("Courier")

    def __init__(self, id, name, email, roll, master=False):
        self.id = id
        self.name = name
        self.email = email
        self.roll = roll
        self.master = master

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'roll': self.roll,
            'master': self.master,
        }

    def __repr__(self):
        return "User<%d> %s, email: %s, roll: %d, master: %s" % (self.id, self.name, self.email, self.roll, self.master)
