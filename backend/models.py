from extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    staff_name = db.Column(db.String(50), nullable=False)
    staff_rfid = db.Column(db.String(50), nullable=True)

class keys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_rfid = db.Column(db.String(50), nullable=True)
    key_name = db.Column(db.String(50), nullable=True)

class KeyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_rfid = db.Column(db.String(50), nullable=False)
    key_rfid = db.Column(db.String(50), nullable=False)
    checkout_time = db.Column(db.DateTime, default=datetime.utcnow)
    return_time = db.Column(db.DateTime, nullable=True)
    due_time = db.Column(db.DateTime, nullable=False)
    returned = db.Column(db.Boolean, default=False)