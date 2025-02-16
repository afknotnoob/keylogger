from extensions import db
from models import staff
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def add_staff(employee_id, staff_name, staff_rfid=None):
    """ Adds a new staff member to the database """
    with app.app_context():
        new_staff = staff(
            employee_id=employee_id,
            staff_name=staff_name,
            staff_rfid=staff_rfid
        )
        db.session.add(new_staff)
        db.session.commit()
        print(f"Staff {staff_name} added successfully with Employee ID {employee_id}.")

# Example Usage:
if __name__ == "__main__":
    employee_id = input("Enter Employee ID: ")
    staff_name = input("Enter Staff Name: ")
    staff_rfid = input("Enter Staff RFID (optional): ").strip() or None

    add_staff(employee_id, staff_name, staff_rfid)
