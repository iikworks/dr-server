from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc
from middlewares import auth_required, developer_required
from schemas.liquid import LiquidsListSchema, LiquidSchema, LiquidsCreateSchema, LiquidsUpdateSchema
from schemas.filters import FiltersQueryArgsSchema
from models.liquid import Liquid

liquids = Blueprint('liquids', 'liquids', url_prefix='/liquids')


@liquids.route('/')
class Liquids(MethodView):
    @liquids.arguments(FiltersQueryArgsSchema, location='query')
    @liquids.response(LiquidsListSchema, code=200)
    def get(self, arguments):
        order_column = arguments['order']['column']
        order_type = arguments['order']['type']
        
        arguments['filters']['deleted'] = False

        query = Liquid.query.filter_by(**arguments['filters'])
        count = query.count()
        
        query = query.order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        )
        query = query.limit(arguments['per_page']['limit'])
        query = query.offset(arguments['per_page']['offset'])

        return {
            'liquids': query.all(),
            'count': count
        }

    @auth_required
    @developer_required
    @liquids.arguments(LiquidsCreateSchema, location='json')
    @liquids.response(LiquidSchema(only=(
        'prefix', 'title', 'balance', 'unit', 'user', 'used', 'id'
    )), code=200)
    def post(self, data):
        liquid = Liquid(user_id=g.user.id, **data)
        liquid.save()

        return liquid


@liquids.route('/<liquid_id>')
class LiquidsById(MethodView):
    @liquids.response(LiquidSchema(only=(
            'prefix', 'title', 'balance', 'unit', 'user', 'used', 'id'
    )), code=200)
    def get(self, liquid_id):
        liquid = Liquid.query.get_or_404(liquid_id)
        if liquid.deleted:
            return abort(404)

        return liquid

    @auth_required
    @developer_required
    @liquids.arguments(LiquidsUpdateSchema, location='json')
    @liquids.response(LiquidSchema(only=(
            'prefix', 'title', 'balance', 'unit', 'user', 'used', 'id'
    )), code=200)
    def put(self, data, liquid_id):
        liquid = Liquid.query.get_or_404(liquid_id)

        if liquid.deleted:
            return abort(404)

        for key, value in data.items():
            setattr(liquid, key, value)
        if 'prefix' in data:
            if data['prefix'] == '':
                liquid.prefix = None
        liquid.save()

        return liquid

    @auth_required
    @developer_required
    def delete(self, liquid_id):
        liquid = Liquid.query.get_or_404(liquid_id)
        if liquid.deleted:
            return abort(404)

        liquid.deleted = True
        liquid.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
