from marshmallow import Schema, fields, post_load, EXCLUDE, ValidationError
from models.liquid import Liquid


class FiltersQueryArgsSchema(Schema):
    order_column = fields.String(missing='id')
    order_type = fields.String(missing='asc')
    limit = fields.Number(missing=25)
    offset = fields.Number(missing=0)
    date = fields.DateTime(required=False, format='%Y-%m-%d')
    liquid_id = fields.Number(required=False)

    @post_load
    def final_validates(self, data, **kwargs):
        if 'liquid_id' in data:
            liquid = Liquid.query.get(data['liquid_id'])
            if not liquid:
                raise ValidationError('ГСМ не найдено', 'liquid_id')

        filters = {
            'filters': {},
            'data': data,
            'order': {
                'column': data['order_column'],
                'type': data['order_type']
            },
            'per_page': {
                'limit': data['limit'],
                'offset': data['offset']
            }
        }

        return filters

    class Meta:
        unknown = EXCLUDE
