from flask import abort, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc
from middlewares import auth_required, developer_required
from schemas.liquid import LiquidSchema, LiquidsQueryArgsSchema, LiquidsCreateSchema
from models.liquid import Liquid

liquids = Blueprint('liquids', 'liquids', url_prefix='/liquids')


@liquids.route('/')
class Liquids(MethodView):
    @liquids.arguments(LiquidsQueryArgsSchema, location='query')
    @liquids.response(LiquidSchema(many=True, only=(
        'prefix', 'title', 'balance', 'unit', 'user'
    )), code=200)
    def get(self, arguments):
        order_column = arguments["order"]["column"]
        order_type = arguments["order"]["type"]

        return Liquid.query.filter_by(**arguments['filters']).order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        ).all()

    @auth_required
    @developer_required
    @liquids.arguments(LiquidsCreateSchema, location='json')
    @liquids.response(LiquidSchema(only=(
        'prefix', 'title', 'balance', 'unit', 'user'
    )), code=200)
    def post(self, data):
        liquid = Liquid(user_id=g.user.id, **data)
        liquid.save()

        return liquid


@liquids.route('/<liquid_id>')
class LiquidsById(MethodView):
    @liquids.response(LiquidSchema(only=(
            'prefix', 'title', 'balance', 'unit', 'user'
    )), code=200)
    def get(self, liquid_id):
        return Liquid.query.get_or_404(liquid_id)
