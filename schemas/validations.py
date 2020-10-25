import re
from marshmallow import ValidationError
from models.user import User


def name_regex(name):
    if not re.match(r'^(?=\D+$)[\w]+$', name):
        raise ValidationError('Not valid name')


def register_other_validations(data):
    if data['password'] != data['password_repeat']:
        raise ValidationError('Password is incorrectly repeated', 'password_repeat')

    user = User.query.filter_by(email=data['email']).first()
    if user:
        raise ValidationError('E-Mail is not unique', 'email')
