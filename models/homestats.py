import datetime
from . import db


class HomeStats(db.Model):
    __tablename__ = 'homestats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    liquid_id = db.Column(
        db.Integer, db.ForeignKey('liquids.id', ondelete='CASCADE')
    )
    title = db.Column(db.String(200), nullable=False)
    place = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(3), default='exp')
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship('User')
    liquid = db.relationship('Liquid')

    def __str__(self):
        return self.title

    def __init__(self, user_id, liquid_id, title, place, position, stat_type):
        self.user_id = user_id
        self.liquid_id = liquid_id
        self.title = title
        self.place = place
        self.position = position
        self.type = stat_type

    def save(self):
        db.session.add(self)
        db.session.commit()
