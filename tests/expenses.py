import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.liquid import Liquid
from models.vehicle import Vehicle
from models.worker import Worker
from models.expense import Expense


class ExpensesTestCase(TestCase):
    def test_expenses_list_page(self):
        user = User(**{
            'email': 'expenseslist@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=888.50
        )
        liquid.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            model='МАЗ-555102',
            government_number=11
        )
        vehicle.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        expense = Expense(
            user_id=user.id,
            liquid_id=liquid.id,
            expense_type='lc',
            amount=20.00,
            vehicle_id=vehicle.id,
            worker_id=worker.id
        )
        expense.save()

        response = self.app.get('/expenses/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(expense.liquid.id, data['expenses'][0]['liquid']['id'])
        self.assertEqual(expense.vehicle.id, data['expenses'][0]['vehicle']['id'])
        self.assertEqual(expense.worker.id, data['expenses'][0]['worker']['id'])
        self.assertEqual(expense.amount, data['expenses'][0]['amount'])

    def test_expenses_create_page(self):
        user = User(**{
            'email': 'expensescreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/expenses/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/expenses/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        start_liquid_balance = 800.00

        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=start_liquid_balance
        )
        liquid.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            model='МАЗ-555102',
            government_number=11
        )
        vehicle.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        expense_liquid_id = liquid.id
        expense_type = 'lc'
        expense_amount = 55.50
        expense_vehicle_id = vehicle.id
        expense_worker_id = worker.id
        expense_waited_date = '2020-11-11 15:55:00'
        expense_date = '2020-11-11T15:55'
        expense_number = 555

        test_cases = {
            'missing_liquid_id': {
                'data': {
                    'type': expense_type,
                    'amount': expense_amount,
                    'worker_id': expense_worker_id,
                    'vehicle_id': expense_vehicle_id,
                    'date': expense_date,
                    'number': expense_number,
                },
                'status_code': 422
            }, 'missing_amount': {
                'data': {
                    'liquid_id': expense_liquid_id,
                    'type': expense_type,
                    'worker_id': expense_worker_id,
                    'vehicle_id': expense_vehicle_id,
                    'date': expense_date,
                    'number': expense_number,
                },
                'status_code': 422
            }, 'missing_type': {
                'data': {
                    'liquid_id': expense_liquid_id,
                    'worker_id': expense_worker_id,
                    'vehicle_id': expense_vehicle_id,
                    'date': expense_date,
                    'number': expense_number,
                },
                'status_code': 422
            }, 'missing_vehicle_id': {
                'data': {
                    'liquid_id': expense_liquid_id,
                    'type': expense_type,
                    'amount': expense_amount,
                    'worker_id': expense_worker_id,
                    'date': expense_date,
                    'number': expense_number,
                },
                'status_code': 422
            }, 'wrong_date': {
                'data': {
                    'liquid_id': expense_liquid_id,
                    'type': expense_type,
                    'amount': expense_amount,
                    'worker_id': expense_worker_id,
                    'vehicle_id': expense_vehicle_id,
                    'date': 'wrong',
                    'number': expense_number,
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'liquid_id': expense_liquid_id,
                    'type': expense_type,
                    'amount': expense_amount,
                    'worker_id': expense_worker_id,
                    'vehicle_id': expense_vehicle_id,
                    'date': expense_date,
                    'number': expense_number,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/expenses/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(expense_liquid_id, data['liquid']['id'])
                self.assertEqual(expense_worker_id, data['worker']['id'])
                self.assertEqual(expense_vehicle_id, data['vehicle']['id'])
                self.assertEqual(expense_amount, data['amount'])
                self.assertEqual(expense_type, data['type'])
                self.assertEqual(expense_waited_date, data['date'])
                self.assertEqual(expense_number, data['number'])

                self.assertEqual(liquid.balance, start_liquid_balance - data['amount'])

    def test_expense_detail_page(self):
        user = User(**{
            'email': 'expensedetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=888.50
        )
        liquid.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            model='МАЗ-555102',
            government_number=11
        )
        vehicle.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        expense = Expense(
            user_id=user.id,
            liquid_id=liquid.id,
            expense_type='lc',
            amount=20.00,
            vehicle_id=vehicle.id,
            worker_id=worker.id
        )
        expense.save()

        response = self.app.get(f'/expenses/0')
        self.assertEqual(response.status_code, 404)

        expense.deleted = True
        expense.save()

        response = self.app.get(f'/expenses/{expense.id}')
        self.assertEqual(response.status_code, 404)

        expense.deleted = False
        expense.save()

        response = self.app.get(f'/expenses/{expense.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(expense.liquid.id, data['liquid']['id'])
        self.assertEqual(expense.worker.id, data['worker']['id'])
        self.assertEqual(expense.vehicle.id, data['vehicle']['id'])
        self.assertEqual(expense.amount, data['amount'])
        self.assertEqual(expense.type, data['type'])

    def test_expense_edit_page(self):
        user = User(**{
            'email': 'expenseedit@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        liquid_start_balance = 888.50
        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=liquid_start_balance
        )
        liquid.save()

        new_liquid_start_balance = 55.00
        new_liquid = Liquid(
            user_id=user.id,
            title='Масло М10-Г2',
            balance=new_liquid_start_balance
        )
        new_liquid.save()

        wrong_liquid = Liquid(
            user_id=user.id,
            title='Масло М10-Г2',
            balance=0
        )
        wrong_liquid.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            model='МАЗ-555102',
            government_number=11
        )
        vehicle.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        new_vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            model='МАЗ-555102',
            government_number=929
        )
        new_vehicle.save()

        new_worker = Worker(
            user_id=user.id,
            first_name='Петр',
            last_name='Петров',
            patronymic='Петрович'
        )
        new_worker.save()

        expense_start_amount = 20.00
        expense = Expense(
            user_id=user.id,
            liquid_id=liquid.id,
            expense_type='lc',
            amount=expense_start_amount,
            vehicle_id=vehicle.id,
            worker_id=worker.id
        )
        expense.save()

        new_expense_liquid_id = new_liquid.id
        new_expense_amount = 50

        response = self.app.put(f'/expenses/{expense.id}', json={
            'liquid_id': new_expense_liquid_id,
            'amount': new_expense_amount,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'liquid_id': new_expense_liquid_id,
            'amount': new_expense_amount,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/expenses/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        expense.deleted = True
        expense.save()

        response = self.app.delete(f'/expenses/{expense.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        expense.deleted = False
        expense.save()

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'liquid_id': 0,
            'amount': new_expense_amount,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'amount': 2000,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'amount': new_expense_amount,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(liquid.balance, (liquid_start_balance + expense_start_amount) - data['amount'])

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'liquid_id': wrong_liquid.id,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'vehicle_id': 0,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'worker_id': 0,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'vehicle_id': new_vehicle.id,
        })
        self.assertEqual(response.status_code, 200)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'worker_id': new_worker.id,
        })
        self.assertEqual(response.status_code, 200)

        response = self.app.put(f'/expenses/{expense.id}?access_token={token.token}', json={
            'liquid_id': new_expense_liquid_id,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_expense_liquid_id, data['liquid']['id'])
        self.assertEqual(liquid.balance, liquid_start_balance + expense_start_amount)
        self.assertEqual(new_liquid.balance, new_liquid_start_balance - data['amount'])

    def test_expense_delete_page(self):
        user = User(**{
            'email': 'expensedelete@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        liquid_start_balance = 888.50
        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=liquid_start_balance
        )
        liquid.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            model='МАЗ-555102',
            government_number=11
        )
        vehicle.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        expense = Expense(
            user_id=user.id,
            liquid_id=liquid.id,
            expense_type='lc',
            amount=20.00,
            vehicle_id=vehicle.id,
            worker_id=worker.id
        )
        expense.save()

        response = self.app.delete(f'/expenses/{expense.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/expenses/{expense.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/expenses/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        expense.deleted = True
        expense.save()

        response = self.app.delete(f'/expenses/{expense.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        expense.deleted = False
        expense.save()

        response = self.app.delete(f'/expenses/{expense.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
        self.assertEqual(liquid.balance, liquid_start_balance + expense.amount)
