import datetime
from . import db


class Expense(db.Model):
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    liquid_id = db.Column(
        db.Integer, db.ForeignKey('liquids.id', ondelete='CASCADE')
    )
    vehicle_id = db.Column(
        db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'),
        nullable=True
    )
    worker_id = db.Column(
        db.Integer, db.ForeignKey('workers.id', ondelete='CASCADE'),
    )
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(precision=10, asdecimal=False, scale=2), default=0.00)
    number = db.Column(db.Integer, default=0)
    purpose = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    user = db.relationship('User')
    liquid = db.relationship('Liquid')
    vehicle = db.relationship('Vehicle')
    worker = db.relationship('Worker')

    def __str__(self):
        return f'{self.amount} {self.liquid.unit}'

    def __init__(
        self,
        user_id,
        liquid_id,
        expense_type,
        worker_id,
        amount,
        date=datetime.datetime.now(),
        number=0,
        vehicle_id=None,
        purpose=None,
    ):
        self.user_id = user_id
        self.liquid_id = liquid_id
        self.type = expense_type
        self.worker_id = worker_id
        self.amount = amount
        self.date = date
        self.number = number
        self.vehicle_id = vehicle_id
        self.purpose = purpose

    def save(self):
        db.session.add(self)
        db.session.commit()
