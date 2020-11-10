from marshmallow import Schema, fields, validate
from schemas.user import UserSchema


class WorkerSchema(Schema):
    id = fields.Int()
    first_name = fields.String()
    last_name = fields.String()
    patronymic = fields.String()
    show_full_name = fields.Boolean()
    used = fields.Integer()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    created_at = fields.String()


class WorkersListSchema(Schema):
    workers = fields.Nested(WorkerSchema(many=True, only=(
        'first_name',
        'last_name',
        'patronymic',
        'show_full_name',
        'user',
        'used',
        'id'
    )))
    count = fields.Integer()


class WorkersCreateSchema(Schema):
    first_name = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )
    last_name = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )
    patronymic = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    show_full_name = fields.Boolean(
        required=False,
    )
    used = fields.Integer(required=False)


class WorkersUpdateSchema(Schema):
    first_name = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    last_name = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    patronymic = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    show_full_name = fields.Boolean(
        required=False,
    )
    used = fields.Integer(required=False)
