from marshmallow import Schema, fields, post_load, EXCLUDE, validate
from schemas.user import UserSchema


class LiquidSchema(Schema):
    id = fields.Int()
    prefix = fields.String()
    title = fields.String()
    balance = fields.Number()
    unit = fields.String()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    created_at = fields.DateTime()


class LiquidsQueryArgsSchema(Schema):
    order_column = fields.String(missing='id')
    order_type = fields.String(missing='asc')

    @post_load
    def final_validates(self, data, **kwargs):
        return {
            'filters': {},
            'order': {
                'column': data['order_column'],
                'type': data['order_type']
            }
        }

    class Meta:
        unknown = EXCLUDE


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
        validate=[validate.Length(max=120, min=1)]
    )
    title = fields.String(
        validate=[validate.Length(max=120, min=1)]
    )
    balance = fields.Decimal(
        places=2
    )
    unit = fields.String(
        validate=[validate.Length(max=50, min=1)]
    )
    used = fields.Integer()
