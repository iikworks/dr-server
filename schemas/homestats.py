from marshmallow import Schema, fields, post_load, EXCLUDE, validate, validates_schema, ValidationError
from schemas.user import UserSchema
from schemas.liquid import LiquidSchema
from schemas.expense import ExpenseListSchema
from schemas.incoming import IncomingListSchema
from models.liquid import Liquid
from models.homestats import HomeStats
from models.worker import Worker
from models.vehicle import Vehicle


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
    average_expense = fields.Number(required=False)
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
        'created_at',
        'average_expense'
    )))


class HomeStatsUnckeckedList(Schema):
    expenses = fields.Nested(ExpenseListSchema(only=('expenses', 'count', 'amount')))
    incoming = fields.Nested(IncomingListSchema(only=('incoming', 'count', 'amount')))


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


class HomeStatsUsingSchema(Schema):
    id = fields.Int()
    worker_id = fields.Integer()
    vehicle_id = fields.Integer()
    used = fields.Integer()


class HomeStatsUsingList(Schema):
    using = fields.Nested(HomeStatsUsingSchema(many=True, only=('id', 'worker_id', 'vehicle_id', 'used')))


class HomeStatsUsingFilters(Schema):
    vehicle_id = fields.Number(required=False)
    worker_id = fields.Number(required=False)

    @post_load
    def final_validates(self, data, **kwargs):
        if 'vehicle_id' in data:
            vehicle = Vehicle.query.get(data['vehicle_id'])
            if not vehicle:
                raise ValidationError('Техника не найдена', 'vehicle_id')

        if 'worker_id' in data:
            worker = Worker.query.get(data['worker_id'])
            if not worker:
                raise ValidationError('Работник не найден', 'worker_id')

        return data

    class Meta:
        unknown = EXCLUDE
