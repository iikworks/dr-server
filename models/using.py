import datetime
from . import db


class Using(db.Model):
    __tablename__ = 'using'

    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(
        db.Integer, db.ForeignKey('workers.id', ondelete='CASCADE'),
    )
    vehicle_id = db.Column(
        db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'),
        nullable=True
    )
    used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    def __init__(self, worker_id, vehicle_id):
        self.worker_id = worker_id
        self.vehicle_id = vehicle_id
        self.used = 0

    def save(self):
        db.session.add(self)
        db.session.commit()
