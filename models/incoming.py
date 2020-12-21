import datetime
from . import db


class Incoming(db.Model):
    __tablename__ = 'incoming'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    liquid_id = db.Column(
        db.Integer, db.ForeignKey('liquids.id', ondelete='CASCADE')
    )
    amount = db.Column(db.Numeric(precision=10, asdecimal=False, scale=2), default=0.00)
    number = db.Column(db.Integer, default=0)
    from_who = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    verified = db.Column(db.Integer, default=0)
    user = db.relationship('User')
    liquid = db.relationship('Liquid')

    def __str__(self):
        return f'{self.amount} {self.liquid.unit} от {self.from_who}'

    def __init__(self, user_id, liquid_id, amount, from_who, date=datetime.datetime.now(), number=0):
        self.user_id = user_id
        self.liquid_id = liquid_id
        self.amount = amount
        self.from_who = from_who
        self.date = date
        self.number = number

    def save(self):
        db.session.add(self)
        db.session.commit()
