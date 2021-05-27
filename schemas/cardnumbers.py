from marshmallow import Schema, fields, validate
from schemas.user import UserSchema


class CardNumberSchema(Schema):
    id = fields.Int()
    title = fields.String()
    number = fields.Integer()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    created_at = fields.String()


class CardNumbersListSchema(Schema):
    cardnumbers = fields.Nested(CardNumberSchema(many=True, only=(
        'title',
        'number',
        'user',
        'created_at',
        'id'
    )))


class CardNumbersCreateSchema(Schema):
    title = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )


class CardNumbersUpdateSchema(Schema):
    title = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    number = fields.Integer(required=False)
