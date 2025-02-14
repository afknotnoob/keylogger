from flask import Flask, Blueprint, request, jsonify, session, send_from_directory
from extensions import *
from models import *
from datetime import datetime, timedelta

routes = Blueprint('routes', __name__)
bcrypt = Bcrypt()

@routes.route('/')
@routes.route('/login')
def serve_login():
    return send_from_directory('../frontend', 'login.html')

@routes.route('/dashboard')
def serve_dashboard():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401  # Prevent unauthorized access
    return send_from_directory('../frontend', 'dashboard.html')

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()  # Fetch user from DB

    if user and bcrypt.check_password_hash(user.password, password):
        session["user"] = email  # Store user session
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 500

@routes.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"redirect": "/login"})

@routes.route('/checkout', methods=['POST'])
def checkout_key():
    data = request.json
    staff_rfid = data.get('staff_rfid')
    key_rfid = data.get('key_rfid')
    duration = int(data.get('duration'))
        
    if not staff_rfid or not key_rfid or not duration:
        return jsonify({'message': 'Missing required fields'}), 400
        
    checkout_time = datetime.utcnow()
    due_time = checkout_time + timedelta(minutes=duration)
        
    new_log = KeyLog(staff_rfid=staff_rfid, key_rfid=key_rfid, checkout_time=checkout_time, due_time=due_time, returned=False)
    db.session.add(new_log)
    db.session.commit()
        
    return jsonify({'message': 'Key checked out successfully'})

@routes.route('/return', methods=['POST'])
def return_key():
    data = request.json
    staff_rfid = data.get('staff_rfid')
    key_rfid = data.get('key_rfid')
        
    if not staff_rfid or not key_rfid:
        return jsonify({'message': 'Missing required fields'}), 400
        
    log_entry = KeyLog.query.filter_by(staff_rfid=staff_rfid, key_rfid=key_rfid, returned=False).first()
        
    if not log_entry:
        return jsonify({'message': 'No active checkout found for this key'}), 404
        
    log_entry.returned = True
    db.session.commit()
        
    return jsonify({'message': 'Key returned successfully'})
    
@routes.route('/logs', methods=['GET'])
def fetch_logs():
    logs = KeyLog.query.all()
    log_list = [{
        'staff_rfid': log.staff_rfid,
        'key_rfid': log.key_rfid,
        'checkout_time': log.checkout_time.strftime('%Y-%m-%d %H:%M:%S'),
        'due_time': log.due_time.strftime('%Y-%m-%d %H:%M:%S'),
        'returned': log.returned
    } for log in logs]
        
    return jsonify(log_list)

@routes.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)