from marshmallow import Schema, fields, post_load, EXCLUDE


class FiltersQueryArgsSchema(Schema):
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
