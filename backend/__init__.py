from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt
from config import Config
from models import db, KeyLog
from routes import routes
import threading
import time
from datetime import datetime

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    Session(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes)

    return app

def send_reminders():
    while True:
        now = datetime.utcnow()
        logs = KeyLog.query.filter(KeyLog.due_time < now, KeyLog.returned == False).all()
        for log in logs:
            print(f"Reminder: Staff {log.staff_rfid} should return key {log.key_rfid}!")
        time.sleep(300)

    reminder_thread = threading.Thread(target=send_reminders, daemon=True)
    reminder_thread.start()