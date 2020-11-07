from marshmallow import Schema, fields, validate
from schemas.user import UserSchema


class VehicleSchema(Schema):
    id = fields.Int()
    type = fields.String()
    title = fields.String()
    government_number = fields.Number()
    used = fields.Integer()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    created_at = fields.String()


class VehiclesListSchema(Schema):
    vehicles = fields.Nested(VehicleSchema(many=True, only=('type', 'title', 'government_number', 'user', 'used', 'id')))
    count = fields.Integer()


class VehiclesCreateSchema(Schema):
    type = fields.String(
        required=True,
        validate=[validate.Length(max=50, min=1), validate.OneOf(['tractor', 'car', 'harvester', 'other'])]
    )
    title = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )
    government_number = fields.Integer(
        required=False,
        validate=[validate.Range(min=0, max=9999)]
    )
    used = fields.Integer(required=False)


class VehiclesUpdateSchema(Schema):
    type = fields.String(
        required=False,
        validate=[validate.Length(max=50, min=1), validate.OneOf(['tractor', 'car', 'harvester', 'other'])]
    )
    title = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    government_number = fields.Integer(
        required=False,
        validate=[validate.Range(min=0, max=9999)]
    )
    used = fields.Integer(required=False)