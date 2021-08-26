from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc
from middlewares import auth_required, developer_required
from schemas.filters import FiltersQueryArgsSchema
from schemas.user import UsersListSchema, UserSchema
from models.user import User

users = Blueprint('users', 'users', url_prefix='/users')


@users.route('/')
class Users(MethodView):
    @users.arguments(FiltersQueryArgsSchema, location='query')
    @users.response(200, UsersListSchema)
    def get(self, arguments):
        order_column = arguments['order']['column']
        order_type = arguments['order']['type']

        arguments['filters']['deleted'] = False

        query = User.query.filter_by(**arguments['filters'])
        count = query.count()

        query = query.order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        )
        if arguments['per_page']['limit'] != 0:
            query = query.limit(arguments['per_page']['limit'])
            query = query.offset(arguments['per_page']['offset'])

        return {
            'users': query.all(),
            'count': count
        }


@users.route('/<user_id>')
class UsersById(MethodView):
    @users.response(200, UserSchema(only=(
        'first_name',
        'last_name',
        'employee',
        'created_at',
        'id'
    )))
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        if user.deleted:
            return abort(404)

        return user
