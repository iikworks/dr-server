from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from schemas.user import UserSchema
from schemas.liquid import LiquidSchema
from models.liquid import Liquid


class IncomingSchema(Schema):
    id = fields.Int()
    amount = fields.Number()
    number = fields.Integer()
    from_who = fields.String()
    date = fields.String()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    liquid = fields.Nested(LiquidSchema(only=('prefix', 'title', 'balance', 'unit', 'user', 'used', 'id')))
    created_at = fields.String()


class IncomingListSchema(Schema):
    incoming = fields.Nested(IncomingSchema(many=True, only=(
        'amount',
        'number',
        'from_who',
        'date',
        'user',
        'liquid',
        'id',
        'created_at'
    )))
    count = fields.Integer()
    amount = fields.Integer(required=False)
    liquid = fields.Nested(
        LiquidSchema(only=('prefix', 'title', 'balance', 'unit', 'user', 'used', 'id')), required=False
    )


class IncomingCreateSchema(Schema):
    amount = fields.Decimal(
        required=True,
        places=2
    )
    number = fields.Integer(required=False)
    from_who = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )
    date = fields.DateTime(format='%Y-%m-%dT%H:%M', required=False)
    liquid_id = fields.Integer(required=True)

    @validates_schema
    def final_validations(self, data, **kwargs):
        liquid = Liquid.query.get(data['liquid_id'])
        if not liquid:
            raise ValidationError('ГСМ не найдено', 'liquid_id')


class IncomingUpdateSchema(Schema):
    amount = fields.Decimal(
        required=False,
        places=2
    )
    number = fields.Integer(required=False)
    from_who = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    date = fields.DateTime(format='%Y-%m-%dT%H:%M', required=False)
    liquid_id = fields.Integer(required=False)

    @validates_schema
    def final_validations(self, data, **kwargs):
        if 'liquid_id' in data:
            liquid = Liquid.query.get(data['liquid_id'])
            if not liquid:
                raise ValidationError('ГСМ не найдено', 'liquid_id')
