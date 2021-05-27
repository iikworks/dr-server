import datetime
from . import db


class CardNumber(db.Model):
    __tablename__ = 'cardnumbers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    title = db.Column(db.String(200), nullable=False)
    number = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship('User')

    def __init__(self, user_id, title):
        self.user_id = user_id
        self.title = title
    
    def save(self):
        db.session.add(self)
        db.session.commit()