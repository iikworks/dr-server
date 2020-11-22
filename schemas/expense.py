from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from schemas.user import UserSchema
from schemas.liquid import LiquidSchema
from models.liquid import Liquid
from models.vehicle import Vehicle
from models.worker import Worker
from schemas.vehicle import VehicleSchema
from schemas.worker import WorkerSchema


class ExpenseSchema(Schema):
    id = fields.Int()
    type = fields.String()
    amount = fields.Number()
    number = fields.Integer()
    purpose = fields.String()
    date = fields.String()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    liquid = fields.Nested(LiquidSchema(only=('prefix', 'title', 'balance', 'unit', 'user', 'used', 'id')))
    vehicle = fields.Nested(VehicleSchema(only=(
        'type',
        'title',
        'government_number',
        'user',
        'used',
        'id',
        'type_display'
    )))
    worker = fields.Nested(WorkerSchema(only=(
        'first_name',
        'last_name',
        'patronymic',
        'show_full_name',
        'user',
        'used',
        'id'
    )))
    created_at = fields.String()


class ExpenseListSchema(Schema):
    expenses = fields.Nested(ExpenseSchema(many=True, only=(
        'type',
        'amount',
        'number',
        'purpose',
        'date',
        'user',
        'liquid',
        'vehicle',
        'worker',
        'id',
        'created_at'
    )))
    count = fields.Integer()
    amount = fields.Integer(required=False)


class ExpenseCreateSchema(Schema):
    type = fields.String(
        required=True,
        validate=[validate.Length(max=50, min=1), validate.OneOf(['lc', 'ic'])]
    )
    amount = fields.Decimal(
        required=True,
        places=2
    )
    number = fields.Integer(required=False)
    purpose = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )

    date = fields.DateTime(format='%Y-%m-%dT%H:%M', required=False)
    liquid_id = fields.Integer(required=True)
    vehicle_id = fields.Integer(required=False)
    worker_id = fields.Integer(required=True)

    @validates_schema
    def final_validations(self, data, **kwargs):
        liquid = Liquid.query.get(data['liquid_id'])
        if not liquid:
            raise ValidationError('ГСМ не найдено', 'liquid_id')

        if data['amount'] > liquid.balance:
            raise ValidationError('Недостаточно топлива', 'liquid_id')

        worker = Worker.query.get(data['worker_id'])
        if not worker:
            raise ValidationError('Работник не найден', 'worker_id')

        if data['type'] == 'lc':
            if 'vehicle_id' not in data:
                raise ValidationError('Техника не найдена', 'vehicle_id')

            vehicle = Vehicle.query.get(data['vehicle_id'])
            if not vehicle:
                raise ValidationError('Техника не найдена', 'vehicle_id')
        elif data['type'] == 'ic':
            if 'purpose' not in data:
                raise ValidationError('Вы не указали назначение', 'purpose')


class ExpenseUpdateSchema(Schema):
    type = fields.String(
        required=False,
        validate=[validate.Length(max=50, min=1), validate.OneOf(['lc', 'ic'])]
    )
    amount = fields.Decimal(
        required=False,
        places=2
    )
    number = fields.Integer(required=False)
    purpose = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )

    date = fields.DateTime(format='%Y-%m-%dT%H:%M', required=False)
    liquid_id = fields.Integer(required=False)
    vehicle_id = fields.Integer(required=False)
    worker_id = fields.Integer(required=False)

    @validates_schema
    def final_validations(self, data, **kwargs):
        if 'liquid_id' in data:
            liquid = Liquid.query.get(data['liquid_id'])
            if not liquid:
                raise ValidationError('ГСМ не найдено', 'liquid_id')

        if 'worker_id' in data:
            worker = Worker.query.get(data['worker_id'])
            if not worker:
                raise ValidationError('Работник не найден', 'worker_id')

        if 'type' in data:
            if data['type'] == 'lc' and 'vehicle_id' in data:
                vehicle = Vehicle.query.get(data['vehicle_id'])
                if not vehicle:
                    raise ValidationError('Техника не найдена', 'vehicle_id')

        if 'vehicle_id' in data:
            vehicle = Vehicle.query.get(data['vehicle_id'])
            if not vehicle:
                raise ValidationError('Техника не найдена', 'vehicle_id')
