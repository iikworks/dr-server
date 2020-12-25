from marshmallow import Schema, fields
from schemas.user import UserSchema


class InviteSchema(Schema):
    id = fields.Int()
    code = fields.String()
    used = fields.Boolean()
    used_at = fields.String()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    created_at = fields.String()


class InvitesListSchema(Schema):
    invites = fields.Nested(InviteSchema(many=True, only=(
        'code',
        'used',
        'used_at',
        'user',
        'created_at',
        'id',
    )))


class InviteUpdateSchema(Schema):
    used = fields.Boolean(required=False)
