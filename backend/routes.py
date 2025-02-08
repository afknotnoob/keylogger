from flask import Blueprint, request, jsonify, session
from models import db, User, KeyLog
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

routes = Blueprint('routes', __name__)
bcrypt = Bcrypt()

@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Logon successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@routes.route('/logout', methods=["POST"])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})

@routes.route('/checkout', methods=['POST'])
def checkout_key():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    due_time = datetime.utcnow() + timedelta(minutes=data['duration'])
    new_log = KeyLog(staff_rfid=data['staff_rfid'], key_rfid=data['key_rfid'], due_time=due_time)
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"message": "Key checked out successfully", "due_time": due_time.isoformat()})

@routes.route('/return', methods=['POST'])
def return_key():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"})
    data = request.get_json()
    log = KeyLog.query.filter_by(staff_rfid=data['staff_rfid'], key_rfid=data['key_rfid'], returned=False).first()
    if log:
        log.return_time = datetime.utcnow()
        log.returned = True
        db.session.commit()
        return jsonify({"message": "Key returned successfully"})
    return jsonify({"message": "No active checkout found"}), 404

@routes.route('/logs', methods=['GET'])
def get_logs():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"})
    logs = KeyLog.query.all()
    log_list = [{
        "staff_rfid": log.staff_rfid,
        "key_rfid": log.key_rfid,
        "checkout_time": log.checkout_time.isoformat(),
        "due_time": log.due_time.isoformat(),
        "return_time": log.return_time.isoformat() if log.return_time else None,
        "returned": log.returned
    } for log in logs]
    return jsonify(log_list)