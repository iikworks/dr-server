import datetime
from . import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    government_number = db.Column(db.Integer, nullable=True)
    used = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship('User')

    def __str__(self):
        if self.government_number:
            return f'{self.title}'

        return self.title

    def __init__(self, user_id, v_type, title, government_number=0):
        self.user_id = user_id
        self.type = v_type
        self.title = title

        if government_number != 0:
            self.government_number = government_number

    def save(self):
        db.session.add(self)
        db.session.commit()
