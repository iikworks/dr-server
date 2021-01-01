from marshmallow import Schema, fields, validate
from schemas.user import UserSchema


class PostSchema(Schema):
    id = fields.Int()
    title = fields.String()
    text = fields.String()
    views = fields.Integer()
    user = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name', 'employee')))
    created_at = fields.String()


class PostsListSchema(Schema):
    posts = fields.Nested(PostSchema(many=True, only=(
        'title',
        'text',
        'user',
        'views',
        'created_at',
        'id'
    )))
    count = fields.Integer()


class PostsCreateSchema(Schema):
    title = fields.String(
        required=True,
        validate=[validate.Length(max=200, min=1)]
    )
    text = fields.String(
        required=True
    )
    views = fields.Integer(required=False)


class PostsUpdateSchema(Schema):
    title = fields.String(
        required=False,
        validate=[validate.Length(max=200, min=1)]
    )
    text = fields.String(
        required=False
    )
    views = fields.Integer(required=False)
