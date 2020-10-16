import bcrypt
from datetime import datetime
from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    employee = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __str__(self):
        return self.email

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return bcrypt.checkpw(str.encode(password), str.encode(self.password))

    def set_password(self, password):
        hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def save(self):
        db.session.add(self)
        db.session.commit()
