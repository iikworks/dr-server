import datetime
from app.helpers import get_random_string
from . import db


class Invite(db.Model):
    __tablename__ = 'invites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True
    )
    code = db.Column(db.String(8), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User')

    def __str__(self):
        return self.code

    def __init__(self):
        self.generate_code()

    def generate_code(self):
        code_string = ''

        while code_string == '':
            temp_code = get_random_string(8)

            invite = Invite.get_by_code(temp_code)
            if invite is None:
                code_string = temp_code

        self.code = code_string

    def set_used(self, user_id):
        self.user_id = user_id
        self.used = True
        self.used_at = datetime.datetime.now()

    @staticmethod
    def get_by_code(code):
        return Invite.query.filter_by(code=code).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
