import decimal

from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc, Date, cast, and_
from middlewares import auth_required, developer_required
from schemas.expense import ExpenseSchema, ExpenseListSchema, ExpenseCreateSchema, ExpenseUpdateSchema
from schemas.filters import FiltersQueryArgsSchema
from models.expense import Expense
from models.liquid import Liquid
from models.worker import Worker
from models.vehicle import Vehicle
from models.using import Using
from datetime import timedelta

expenses = Blueprint('expenses', 'expenses', url_prefix='/expenses')


@expenses.route('/')
class ExpensesList(MethodView):
    @expenses.arguments(FiltersQueryArgsSchema, location='query')
    @expenses.response(200, ExpenseListSchema)
    def get(self, arguments):
        # Ресурс для показа всех расходов
        # Принимает (query): order_column, order_type, limit, offset, unverified,
        ##  archive, date, s_date, e_date, liquid_id, vehicle_id, worker_id
        # Возвращает: expenses, count, amount, liquid

        # Фильтры для упорядовачиния результата
        order_column = arguments['order']['column']
        order_type = arguments['order']['type']

        # Фильтр для скрытия удаленных записей
        arguments['filters']['deleted'] = False

        # Устанвливается фильтр delete=true, если необходимо показать архив
        if 'archive' in arguments['data']:
            arguments['filters']['deleted'] = True

        # Применение фильтров
        query = Expense.query.filter_by(**arguments['filters'])

        response = {}

        # Фильтр по определенной дате
        if 'date' in arguments['data']:
            query = query.filter(cast(Expense.date, Date) == arguments['data']['date'])

        # Фильтр по периоду даты
        if 's_date' in arguments['data'] and 'e_date' in arguments['data']:
            query = query.filter(
                and_(Expense.date <= arguments['data']['e_date'] + timedelta(days=1), Expense.date >= arguments['data']['s_date'])
            )

        # Фильтр по технике
        if 'vehicle_id' in arguments['data']:
            query = query.filter_by(vehicle_id=arguments['data']['vehicle_id'])

        # Фильтр по работнику
        if 'worker_id' in arguments['data']:
            query = query.filter_by(worker_id=arguments['data']['worker_id'])

        # Фильтр по степени проверки     
        if 'unverified' in arguments['data']:
            query = query.filter(Expense.verified != 2)

        # Фильтр по ГСМ
        if 'liquid_id' in arguments['data']:
            query = query.filter_by(liquid_id=arguments['data']['liquid_id'])

            # Подсчет общего количества расхода жидкости по единице измерения

            amounts = query.with_entities(Expense.amount)
            amount = 0

            for expenseAmount in amounts:
                amount = amount + expenseAmount.amount

            response['amount'] = amount
            response['liquid'] = Liquid.query.get(arguments['data']['liquid_id'])
        
        
        # Подсчет количества расходов
        count = query.count()

        # Упорядочение расходов по колонке
        query = query.order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        )
        
        # Лимит и оффсет выдачи для пагинации
        if arguments['per_page']['limit'] != 0:
            query = query.limit(arguments['per_page']['limit'])
            query = query.offset(arguments['per_page']['offset'])
        
        # Возврат результата
        response['expenses'] = query.all()
        response['count'] = count

        return response

    @auth_required
    @developer_required
    @expenses.arguments(ExpenseCreateSchema, location='json')
    @expenses.response(200, ExpenseSchema(only=(
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
        'verified',
        'created_at'
    )))
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

            using = Using.query.filter_by(worker_id=worker.id, vehicle_id=vehicle.id).first()
            if not using:
                using = Using(worker_id=worker.id, vehicle_id=vehicle.id)
            
            using.used = using.used + 1
            using.save()

        return expense


@expenses.route('/<expense_id>')
class ExpenseById(MethodView):
    @expenses.response(200, ExpenseSchema(only=(
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
        'verified',
        'created_at'
    )))
    def get(self, expense_id):
        expense = Expense.query.get_or_404(expense_id)
        if expense.deleted:
            return abort(404)

        return expense

    @auth_required
    @developer_required
    @expenses.arguments(ExpenseUpdateSchema, location='json')
    @expenses.response(200, ExpenseSchema(only=(
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
        'verified',
        'created_at'
    )))
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
        
        using = Using.query.filter_by(worker_id=expense.worker_id, vehicle_id=expense.vehicle_id).first()
        if not using:
            using = Using(worker_id=expense.worker_id, vehicle_id=expense.vehicle_id)
        
        using.used = using.used + 1
        using.save()

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
