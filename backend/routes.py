from flask import Blueprint, request, jsonify, session, send_from_directory
from extensions import *
from models import User

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

    # Remove authentication check, just assume login is successful
    session["user"] = email  # Store user session
    return jsonify({"message": "Login successful"})

@routes.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"redirect": "/login"})

@routes.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)