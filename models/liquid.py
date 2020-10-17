import datetime
from . import db


class Liquid(db.Model):
    __tablename__ = 'liquids'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    prefix = db.Column(db.String(120))
    title = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Numeric(precision=2, asdecimal=False, decimal_return_scale=None), default=0.00)
    unit = db.Column(db.String(50), default='л')
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship('User')

    def __str__(self):
        return self.title

    def __init__(self, user_id, title, prefix='', balance=0.00, unit='л'):
        self.user_id = user_id
        self.title = title
        self.balance = balance
        self.unit = unit

        if prefix != '':
            self.prefix = prefix

    def save(self):
        db.session.add(self)
        db.session.commit()
