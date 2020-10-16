import datetime
from app.helpers import get_random_string
from . import db


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    token = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    expires_in = db.Column(db.DateTime, default=datetime.datetime.now() + datetime.timedelta(days=31), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    user = db.relationship('User')

    def __str__(self):
        return self.token

    def __init__(self, user_id):
        self.user_id = user_id
        self.generate_token()

    def generate_token(self):
        token_string = ''

        while token_string == '':
            temp_token = get_random_string(64)

            token = Token.get_by_token(temp_token)
            if token is None:
                token_string = temp_token

        self.token = token_string

    @staticmethod
    def get_by_token(token):
        return Token.query.filter_by(token=token).first()

    def is_token_has_no_expires(self):
        if self.deleted:
            return False

        current_date = datetime.datetime.now()
        return current_date < self.expires_in

    def delete(self):
        self.deleted = True
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
