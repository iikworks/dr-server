from marshmallow import Schema, fields, post_load, EXCLUDE, validate
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


class LiquidsQueryArgsSchema(Schema):
    order_column = fields.String(missing='id')
    order_type = fields.String(missing='asc')
    limit = fields.Number(missing=25)
    offset = fields.Number(missing=0)

    @post_load
    def final_validates(self, data, **kwargs):
        return {
            'filters': {},
            'order': {
                'column': data['order_column'],
                'type': data['order_type']
            },
            'per_page': {
                'limit': data['limit'],
                'offset': data['offset']
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
