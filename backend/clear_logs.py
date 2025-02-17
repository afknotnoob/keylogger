import sys
from extensions import db
from models import User, staff, keys, KeyLog
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def clear_table(table_name):
    with app.app_context():
        model_mapping = {
            "User": User,
            "staff": staff,
            "keys": keys,
            "KeyLog": KeyLog
        }
        
        model = model_mapping.get(table_name)
        if model:
            db.session.query(model).delete()
            db.session.commit()
            print(f"All entries in {table_name} have been deleted.")
        else:
            print("Invalid table name provided.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clear_table.py <table_name>")
    else:
        clear_table(sys.argv[1])
