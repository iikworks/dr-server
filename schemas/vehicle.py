from marshmallow import Schema, fields, validate, validates_schema
from models.worker import Worker
from schemas.user import UserSchema
from schemas.worker import WorkerSchema


class VehicleSchema(Schema):
    id = fields.Int()
    type = fields.String()
    type_display = fields.Method('display_type')
    brand = fields.String()
    model = fields.String()
    government_number = fields.Number()
    government_number_letters = fields.String()
    government_number_region = fields.Number()
    year_of_ussue = fields.Number()
    used = fields.Integer()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
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

    def display_type(self, obj):
        types = {
            'tractor': 'Тр',
            'car': 'Авт',
            'harvester': 'Сх',
            'other': 'Др'
        }

        return types[obj.type]


class VehiclesListSchema(Schema):
    vehicles = fields.Nested(VehicleSchema(many=True, only=(
        'type',
        'brand',
        'model',
        'government_number',
        'government_number_letters',
        'government_number_region',
        'year_of_ussue',
        'user',
        'worker',
        'used',
        'id',
        'type_display'
    )))
    count = fields.Integer()


class VehiclesCreateSchema(Schema):
    type = fields.String(
        required=True,
        validate=[validate.Length(max=50, min=1), validate.OneOf(['tractor', 'car', 'harvester', 'other'])]
    )
    brand = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    model = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )
    government_number = fields.Integer(
        required=False,
        validate=[validate.Range(min=0, max=9999)]
    )
    government_number_letters = fields.String(
        required=False,
        validate=[validate.Length(max=2, min=2)]
    )
    government_number_region = fields.Integer(
        required=False,
        validate=[validate.Range(min=0, max=7)]
    )
    year_of_ussue = fields.Integer(
        required=False,
        validate=[validate.Range(min=1900, max=2100)]
    )
    worker_id = fields.Integer(required=False)
    used = fields.Integer(required=False)

    @validates_schema
    def final_validations(self, data, **kwargs):
        if 'worker_id' in data:
            worker = Worker.query.get(data['worker_id'])
            if not worker:
                raise ValidationError('Работник не найден', 'worker_id')


class VehiclesUpdateSchema(Schema):
    type = fields.String(
        required=False,
        validate=[validate.Length(max=50, min=1), validate.OneOf(['tractor', 'car', 'harvester', 'other'])]
    )
    brand = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    model = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    government_number = fields.Integer(
        required=False,
        validate=[validate.Range(min=0, max=9999)]
    )
    government_number_letters = fields.String(
        required=False,
        validate=[validate.Length(max=2, min=2)]
    )
    government_number_region = fields.Integer(
        required=False,
        validate=[validate.Range(min=0, max=7)]
    )
    year_of_ussue = fields.Integer(
        required=False,
        validate=[validate.Range(min=1900, max=2100)]
    )
    worker_id = fields.Integer(required=False)
    used = fields.Integer(required=False)

    @validates_schema
    def final_validations(self, data, **kwargs):
        if 'worker_id' in data:
            worker = Worker.query.get(data['worker_id'])
            if not worker:
                raise ValidationError('Работник не найден', 'worker_id')
