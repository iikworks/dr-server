import datetime
from . import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(200), nullable=True)
    model = db.Column(db.String(200), nullable=False)
    government_number = db.Column(db.Integer, nullable=True)
    government_number_letters = db.Column(db.String(2), nullable=True)
    government_number_region = db.Column(db.Integer, nullable=True)
    year_of_ussue = db.Column(db.Integer, nullable=True)
    worker_id = db.Column(
        db.Integer, db.ForeignKey('workers.id', ondelete='CASCADE'),
        nullable=True
    )
    used = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship('User')
    worker = db.relationship('Worker')

    def __str__(self):
        if self.government_number:
            return f'{self.model}'

        return self.model

    def __init__(self,
            user_id,
            v_type,
            model,
            government_number=0,
            brand=None,
            government_number_region=0,
            government_number_letters=None,
            year_of_ussue=0,
            worker_id=0
        ):
        self.user_id = user_id
        self.type = v_type
        self.model = model

        if government_number != 0:
            self.government_number = government_number

        if brand:
            self.brand = brand

        if government_number_region != 0:
            self.government_number_region = government_number_region

        if government_number_letters:
            self.government_number_letters = government_number_letters

        if year_of_ussue != 0:
            self.year_of_ussue = year_of_ussue

        if worker_id != 0:
            self.worker_id = worker_id

    def save(self):
        db.session.add(self)
        db.session.commit()
