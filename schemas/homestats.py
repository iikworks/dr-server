from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from schemas.user import UserSchema
from schemas.liquid import LiquidSchema
from schemas.expense import ExpenseListSchema
from schemas.incoming import IncomingListSchema
from models.liquid import Liquid
from models.homestats import HomeStats


class HomeStatsSchema(Schema):
    id = fields.Int()
    type = fields.String()
    type_display = fields.Method('display_type')
    title = fields.String()
    place = fields.Integer()
    position = fields.Integer()
    expenses = fields.Nested(ExpenseListSchema(only=('expenses', 'count', 'amount')))
    incoming = fields.Nested(IncomingListSchema(only=('incoming', 'count', 'amount')))
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    liquid = fields.Nested(LiquidSchema(only=('prefix', 'title', 'balance', 'unit', 'user', 'used', 'id')))
    created_at = fields.String()

    def display_type(self, obj):
        types = {
            'exp': 'Расход',
            'inc': 'Приход',
        }

        return types[obj.type]


class HomeStatsListSchema(Schema):
    homestats = fields.Nested(HomeStatsSchema(many=True, only=(
        'type',
        'type_display',
        'title',
        'place',
        'position',
        'expenses',
        'incoming',
        'liquid',
        'id',
        'user',
        'created_at'
    )))


class HomeStatsCreateSchema(Schema):
    type = fields.String(
        required=True,
        validate=[validate.Length(max=3, min=1), validate.OneOf(['exp', 'inc'])]
    )
    title = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )
    place = fields.Integer(required=True)
    position = fields.Integer(required=True)
    liquid_id = fields.Integer(required=True)

    @validates_schema
    def final_validations(self, data, **kwargs):
        liquid = Liquid.query.get(data['liquid_id'])
        if not liquid:
            raise ValidationError('ГСМ не найдено', 'liquid_id')

        homestat = HomeStats.query.filter_by(deleted=False, place=data['place'], position=data['position']).first()
        if homestat:
            raise ValidationError('Позиция занята', 'position')


class HomeStatsUpdateSchema(Schema):
    type = fields.String(
        required=False,
        validate=[validate.Length(max=3, min=1), validate.OneOf(['exp', 'inc'])]
    )
    title = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    place = fields.Integer(required=False)
    position = fields.Integer(required=False)
    liquid_id = fields.Integer(required=False)

    @validates_schema
    def final_validations(self, data, **kwargs):
        if 'liquid_id' in data:
            liquid = Liquid.query.get(data['liquid_id'])
            if not liquid:
                raise ValidationError('ГСМ не найдено', 'liquid_id')
