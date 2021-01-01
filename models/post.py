import datetime
from . import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship('User')

    def __str__(self):
        return self.title

    def __init__(self, user_id, title, text):
        self.user_id = user_id
        self.title = title
        self.text = text

    def save(self):
        db.session.add(self)
        db.session.commit()
