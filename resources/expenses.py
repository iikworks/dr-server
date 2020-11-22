import decimal

from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc, Date, cast
from middlewares import auth_required, developer_required
from schemas.expense import ExpenseSchema, ExpenseListSchema, ExpenseCreateSchema, ExpenseUpdateSchema
from schemas.filters import FiltersQueryArgsSchema
from models.expense import Expense
from models.liquid import Liquid
from models.worker import Worker
from models.vehicle import Vehicle

expenses = Blueprint('expenses', 'expenses', url_prefix='/expenses')


@expenses.route('/')
class ExpensesList(MethodView):
    @expenses.arguments(FiltersQueryArgsSchema, location='query')
    @expenses.response(ExpenseListSchema, code=200)
    def get(self, arguments):
        order_column = arguments['order']['column']
        order_type = arguments['order']['type']

        arguments['filters']['deleted'] = False

        query = Expense.query.filter_by(**arguments['filters'])

        response = {}

        if 'date' in arguments['data']:
            query = query.filter(cast(Expense.date, Date) == arguments['data']['date'])

        if 'liquid_id' in arguments['data']:
            query = query.filter_by(liquid_id=arguments['data']['liquid_id'])

            amounts = query.with_entities(Expense.amount)
            amount = 0

            for expenseAmount in amounts:
                amount = amount + expenseAmount.amount

            response['amount'] = amount

        count = query.count()

        query = query.order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        )
        query = query.limit(arguments['per_page']['limit'])
        query = query.offset(arguments['per_page']['offset'])

        response['expenses'] = query.all()
        response['count'] = count

        return response

    @auth_required
    @developer_required
    @expenses.arguments(ExpenseCreateSchema, location='json')
    @expenses.response(ExpenseSchema(only=(
        'type',
        'amount',
        'number',
        'purpose',
        'date',
        'user',
        'liquid',
        'vehicle',
        'worker',
        'id',
        'created_at'
    )), code=200)
    def post(self, data):
        liquid = Liquid.query.get(data['liquid_id'])

        data['expense_type'] = data['type']
        del data['type']

        expense = Expense(user_id=g.user.id, **data)
        expense.save()

        liquid.balance = liquid.balance - expense.amount
        liquid.used = liquid.used + 1
        liquid.save()

        worker = Worker.query.get(data['worker_id'])
        worker.used = worker.used + 1
        worker.save()

        if 'vehicle_id' in data:
            vehicle = Vehicle.query.get(data['vehicle_id'])
            vehicle.used = vehicle.used + 1
            vehicle.save()

        return expense


@expenses.route('/<expense_id>')
class ExpenseById(MethodView):
    @expenses.response(ExpenseSchema(only=(
        'type',
        'amount',
        'number',
        'purpose',
        'date',
        'user',
        'liquid',
        'vehicle',
        'worker',
        'id',
        'created_at'
    )), code=200)
    def get(self, expense_id):
        expense = Expense.query.get_or_404(expense_id)
        if expense.deleted:
            return abort(404)

        return expense

    @auth_required
    @developer_required
    @expenses.arguments(ExpenseUpdateSchema, location='json')
    @expenses.response(ExpenseSchema(only=(
        'type',
        'amount',
        'number',
        'purpose',
        'date',
        'user',
        'liquid',
        'vehicle',
        'worker',
        'id',
        'created_at'
    )), code=200)
    def put(self, data, expense_id):
        expense = Expense.query.get_or_404(expense_id)

        if expense.deleted:
            return abort(404)

        if 'amount' in data:
            if expense.amount != data['amount']:
                liquid = Liquid.query.get(expense.liquid.id)

                if liquid.balance < data['amount']:
                    return jsonify({
                        'code': 422,
                        'json': {
                            'amount': 'Недостаточно топлива'
                        },
                        'status': 'Unprocessable Entity'
                    }), 422

                liquid.balance = decimal.Decimal((liquid.balance + expense.amount)) - data['amount']
                liquid.save()
        if 'liquid_id' in data:
            if expense.liquid.id != data['liquid_id']:
                old_liquid = Liquid.query.get(expense.liquid.id)
                new_liquid = Liquid.query.get(data['liquid_id'])

                if new_liquid.balance < expense.amount:
                    return jsonify({
                        'code': 422,
                        'json': {
                            'liquid_id': 'Недостаточно топлива'
                        },
                        'status': 'Unprocessable Entity'
                    }), 422

                old_liquid.balance = old_liquid.balance + expense.amount
                old_liquid.save()

                new_liquid.balance = new_liquid.balance - expense.amount
                new_liquid.used = new_liquid.used + 1
                new_liquid.save()

                expense.liquid_id = new_liquid.id
                expense.save()

        if 'worker_id' in data:
            worker = Worker.query.get(data['worker_id'])
            worker.used = worker.used + 1
            worker.save()

        if 'vehicle_id' in data:
            vehicle = Vehicle.query.get(data['vehicle_id'])
            vehicle.used = vehicle.used + 1
            vehicle.save()

        for key, value in data.items():
            setattr(expense, key, value)

        expense.save()

        return expense

    @auth_required
    @developer_required
    def delete(self, expense_id):
        expense = Expense.query.get_or_404(expense_id)
        if expense.deleted:
            return abort(404)

        expense.deleted = True
        expense.save()

        liquid = Liquid.query.get(expense.liquid.id)
        liquid.balance = liquid.balance + expense.amount
        liquid.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
