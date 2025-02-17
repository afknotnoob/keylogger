from extensions import db
from models import keys
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def add_key(key_rfid, key_name):
    """ Adds a new key to the database """
    with app.app_context():
        new_key = keys(
            key_rfid=key_rfid,
            key_name=key_name
        )
        db.session.add(new_key)
        db.session.commit()
        print(f"Key {key_name} added successfully.")


if __name__ == "__main__":
    key_rfid = input("Enter Key RFID: ").strip() or None
    key_name = input("Enter Key Name:")

    add_key(key_rfid, key_name)
