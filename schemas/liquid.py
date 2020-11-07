from marshmallow import Schema, fields, validate
from schemas.user import UserSchema


class LiquidSchema(Schema):
    id = fields.Int()
    prefix = fields.String()
    title = fields.String()
    balance = fields.Number()
    unit = fields.String()
    used = fields.Integer()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    created_at = fields.String()


class LiquidsListSchema(Schema):
    liquids = fields.Nested(LiquidSchema(many=True, only=('prefix', 'title', 'balance', 'unit', 'user', 'used', 'id')))
    count = fields.Integer()


class LiquidsCreateSchema(Schema):
    prefix = fields.String(
        required=False,
        validate=[validate.Length(max=120, min=1)]
    )
    title = fields.String(
        required=True,
        validate=[validate.Length(max=120, min=1)]
    )
    balance = fields.Decimal(
        required=False,
        places=2
    )
    unit = fields.String(
        required=False,
        validate=[validate.Length(max=50, min=1)]
    )
    used = fields.Integer(required=False)


class LiquidsUpdateSchema(Schema):
    prefix = fields.String(
        required=False,
        validate=[validate.Length(max=120, min=1)]
    )
    title = fields.String(
        required=False,
        validate=[validate.Length(max=120, min=1)]
    )
    balance = fields.Decimal(
        required=False,
        places=2
    )
    unit = fields.String(
        required=False,
        validate=[validate.Length(max=50, min=1)]
    )
    used = fields.Integer(required=False)
