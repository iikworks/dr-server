import decimal

from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc, Date, cast, and_
from middlewares import auth_required, developer_required
from schemas.incoming import IncomingSchema, IncomingListSchema, IncomingCreateSchema, IncomingUpdateSchema
from schemas.filters import FiltersQueryArgsSchema
from models.incoming import Incoming
from models.liquid import Liquid
from datetime import timedelta

incoming = Blueprint('incoming', 'incoming', url_prefix='/incoming')


@incoming.route('/')
class IncomingList(MethodView):
    @incoming.arguments(FiltersQueryArgsSchema, location='query')
    @incoming.response(IncomingListSchema, code=200)
    def get(self, arguments):
        order_column = arguments['order']['column']
        order_type = arguments['order']['type']

        arguments['filters']['deleted'] = False

        query = Incoming.query.filter_by(**arguments['filters'])

        response = {}

        if 'date' in arguments['data']:
            query = query.filter(cast(Incoming.date, Date) == arguments['data']['date'])

        if 's_date' in arguments['data'] and 'e_date' in arguments['data']:
            query = query.filter(
                and_(Incoming.date <= arguments['data']['e_date'] + timedelta(days=1), Incoming.date >= arguments['data']['s_date'])
            )

        if 'liquid_id' in arguments['data']:
            query = query.filter_by(liquid_id=arguments['data']['liquid_id'])

            amounts = query.with_entities(Incoming.amount)
            amount = 0

            for expenseAmount in amounts:
                amount = amount + expenseAmount.amount

            response['amount'] = amount
            response['liquid'] = Liquid.query.get(arguments['data']['liquid_id'])

        count = query.count()

        query = query.order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        )
        if arguments['per_page']['limit'] != 0:
            query = query.limit(arguments['per_page']['limit'])
            query = query.offset(arguments['per_page']['offset'])

        response['incoming'] = query.all()
        response['count'] = count

        return response

    @auth_required
    @developer_required
    @incoming.arguments(IncomingCreateSchema, location='json')
    @incoming.response(IncomingSchema(only=(
        'amount',
        'number',
        'from_who',
        'date',
        'user',
        'liquid',
        'id',
        'created_at'
    )), code=200)
    def post(self, data):
        liquid = Liquid.query.get(data['liquid_id'])

        incoming_model = Incoming(user_id=g.user.id, **data)
        incoming_model.save()

        liquid.balance = liquid.balance + incoming_model.amount
        liquid.used = liquid.used + 1
        liquid.save()

        return incoming_model


@incoming.route('/<incoming_id>')
class IncomingById(MethodView):
    @incoming.response(IncomingSchema(only=(
        'amount',
        'number',
        'from_who',
        'date',
        'user',
        'liquid',
        'id',
        'created_at'
    )), code=200)
    def get(self, incoming_id):
        incoming_model = Incoming.query.get_or_404(incoming_id)
        if incoming_model.deleted:
            return abort(404)

        return incoming_model

    @auth_required
    @developer_required
    @incoming.arguments(IncomingUpdateSchema, location='json')
    @incoming.response(IncomingSchema(only=(
        'amount',
        'number',
        'from_who',
        'date',
        'user',
        'liquid',
        'id',
        'created_at'
    )), code=200)
    def put(self, data, incoming_id):
        incoming_model = Incoming.query.get_or_404(incoming_id)

        if incoming_model.deleted:
            return abort(404)

        if 'amount' in data:
            if incoming_model.amount != data['amount']:
                liquid = Liquid.query.get(incoming_model.liquid.id)
                liquid.balance = decimal.Decimal((liquid.balance - incoming_model.amount)) + data['amount']
                liquid.save()
        if 'liquid_id' in data:
            if incoming_model.liquid.id != data['liquid_id']:
                old_liquid = Liquid.query.get(incoming_model.liquid.id)
                new_liquid = Liquid.query.get(data['liquid_id'])

                old_liquid.balance = old_liquid.balance - incoming_model.amount
                old_liquid.save()

                new_liquid.balance = new_liquid.balance + incoming_model.amount
                new_liquid.used = new_liquid.used + 1
                new_liquid.save()

                incoming_model.liquid_id = new_liquid.id
                incoming_model.save()

        for key, value in data.items():
            setattr(incoming_model, key, value)

        incoming_model.save()

        return incoming_model

    @auth_required
    @developer_required
    def delete(self, incoming_id):
        incoming_model = Incoming.query.get_or_404(incoming_id)
        if incoming_model.deleted:
            return abort(404)

        incoming_model.deleted = True
        incoming_model.save()

        liquid = Liquid.query.get(incoming_model.liquid.id)
        liquid.balance = liquid.balance - incoming_model.amount
        liquid.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
