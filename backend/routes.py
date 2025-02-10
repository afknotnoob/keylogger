from flask import Blueprint, request, jsonify, session, send_from_directory
from extensions import db
from models import User, KeyLog
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os

routes = Blueprint('routes', __name__)
bcrypt = Bcrypt()

@routes.route('/')
@routes.route('/login')
def serve_login():
    return send_from_directory('../frontend', 'login.html')

@routes.route('/dashboard')
def serve_dashboard():
    if 'user_id' not in session:
        return send_from_directory('../frontend', 'login.html')
    return send_from_directory('../frontend', 'dashboard.html')

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"redirect": "/dashboard"})  
    return jsonify({"error": "Invalid credentials"}), 401

@routes.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"redirect": "/login"})

@routes.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)