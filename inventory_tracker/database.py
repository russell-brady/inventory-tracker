from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class ItemSignOut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    subtype = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(300), unique=False)
    deadline = db.Column(db.String(100), unique=False)
    signature = db.Column(db.String(120000), unique=False)
    employee = db.Column(db.String(100), unique=False)
    employee_email = db.Column(db.String(100), unique=False)

    def __init__(self, name, subtype, description, deadline, signature, employee, employee_email):
        self.name = name
        self.subtype = subtype
        self.description = description
        self.deadline = deadline
        self.signature = signature
        self.employee = employee
        self.employee_email = employee_email

    def __repr__(self):
        return '<Item: %r>' % self.description

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

def register_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()