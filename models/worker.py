import datetime
from . import db


class Worker(db.Model):
    __tablename__ = 'workers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    patronymic = db.Column(db.String(200), nullable=True)
    show_full_name = db.Column(db.Boolean, default=False)
    used = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship('User')

    def __str__(self):
        if self.show_full_name:
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        else:
            return f'{self.last_name} {self.first_name[0]}.'

    def __init__(self, user_id, first_name, last_name, patronymic=None, show_full_name=False):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.show_full_name = show_full_name

    def save(self):
        db.session.add(self)
        db.session.commit()
