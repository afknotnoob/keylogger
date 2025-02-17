from flask import Blueprint, request, jsonify, session, send_from_directory
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
    
    staff_member = staff.query.filter_by(staff_rfid=staff_rfid).first()
    if not staff_member:
        return jsonify({'message': 'Staff not found'}), 404
    
    key_item = keys.query.filter_by(key_rfid=key_rfid).first()
    if not key_item:
        return jsonify({'message': 'Key not found'}), 404
        
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
    page = request.args.get('page', 1, type=int)  
    per_page = request.args.get('per_page', 20, type=int) 

    logs = KeyLog.query.order_by(KeyLog.checkout_time.desc()).paginate(page=page, per_page=per_page, error_out=False)

    log_list = []
    for log in logs.items:
        staff_member = staff.query.filter_by(staff_rfid=log.staff_rfid).first()
        key_item = keys.query.filter_by(key_rfid=log.key_rfid).first()
        
        log_list.append({
            'staff_name': staff_member.staff_name if staff_member else 'Unknown',
            'key_name': key_item.key_name if key_item else 'Unknown',
            'checkout_time': log.checkout_time.strftime('%Y-%m-%d %H:%M:%S'),
            'due_time': log.due_time.strftime('%Y-%m-%d %H:%M:%S'),
            'returned': log.returned
        }) 

    return jsonify({
        'logs': log_list,
        'total_logs': logs.total,
        'current_page': logs.page,
        'total_pages': logs.pages,
        'has_next': logs.has_next,
        'has_prev': logs.has_prev,
        'next_page': logs.next_num if logs.has_next else None,
        'prev_page': logs.prev_num if logs.has_prev else None
    })

@routes.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)