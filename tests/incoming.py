import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.liquid import Liquid
from models.incoming import Incoming


class IncomingTestCase(TestCase):
    def test_incoming_list_page(self):
        user = User(**{
            'email': 'incominglist@mail.ru',
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

        incoming = Incoming(
            user_id=user.id,
            liquid_id=liquid.id,
            amount=1.50,
            from_who='Крулевщизна н/б'
        )
        incoming.save()

        response = self.app.get('/incoming/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(incoming.liquid.id, data['incoming'][0]['liquid']['id'])
        self.assertEqual(incoming.amount, data['incoming'][0]['amount'])
        self.assertEqual(incoming.from_who, data['incoming'][0]['from_who'])

    def test_incoming_create_page(self):
        user = User(**{
            'email': 'incomingcreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/incoming/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/incoming/?access_token={token.token}')
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

        incoming_liquid_id = liquid.id
        incoming_amount = 55.50
        incoming_from_who = 'Крулевщизна н/б'
        incoming_waited_date = '2020-11-11 15:55:00'
        incoming_date = '2020-11-11T15:55'
        incoming_number = 555

        test_cases = {
            'missing_liquid_id': {
                'data': {
                    'amount': incoming_amount,
                    'from_who': incoming_from_who,
                    'date': incoming_date,
                    'number': incoming_number,
                },
                'status_code': 422
            }, 'missing_amount': {
                'data': {
                    'liquid_id': incoming_liquid_id,
                    'from_who': incoming_from_who,
                    'date': incoming_date,
                    'number': incoming_number,
                },
                'status_code': 422
            }, 'missing_from_who': {
                'data': {
                    'liquid_id': incoming_liquid_id,
                    'amount': incoming_amount,
                    'date': incoming_date,
                    'number': incoming_number,
                },
                'status_code': 422
            }, 'wrong_date': {
                'data': {
                    'liquid_id': incoming_liquid_id,
                    'amount': incoming_amount,
                    'from_who': incoming_from_who,
                    'date': 'wrong',
                    'number': incoming_number,
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'liquid_id': incoming_liquid_id,
                    'amount': incoming_amount,
                    'from_who': incoming_from_who,
                    'date': incoming_date,
                    'number': incoming_number,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/incoming/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(incoming_liquid_id, data['liquid']['id'])
                self.assertEqual(incoming_amount, data['amount'])
                self.assertEqual(incoming_from_who, data['from_who'])
                self.assertEqual(incoming_waited_date, data['date'])
                self.assertEqual(incoming_number, data['number'])

                self.assertEqual(liquid.balance, data['amount'] + start_liquid_balance)

    def test_incoming_detail_page(self):
        user = User(**{
            'email': 'incomingdetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=800.00
        )
        liquid.save()

        incoming = Incoming(
            user_id=user.id,
            liquid_id=liquid.id,
            amount=1.50,
            from_who='Крулевщизна н/б'
        )
        incoming.save()

        response = self.app.get(f'/incoming/0')
        self.assertEqual(response.status_code, 404)

        incoming.deleted = True
        incoming.save()

        response = self.app.get(f'/incoming/{incoming.id}')
        self.assertEqual(response.status_code, 404)

        incoming.deleted = False
        incoming.save()

        response = self.app.get(f'/incoming/{incoming.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(incoming.liquid.id, data['liquid']['id'])
        self.assertEqual(incoming.amount, data['amount'])
        self.assertEqual(incoming.from_who, data['from_who'])

    def test_incoming_edit_page(self):
        user = User(**{
            'email': 'incomingdetail@mail.ru',
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

        new_liquid_start_balance = 5.00
        new_liquid = Liquid(
            user_id=user.id,
            title='Масло М10-Г2',
            balance=new_liquid_start_balance
        )
        new_liquid.save()

        incoming_start_amount = 1.50
        incoming = Incoming(
            user_id=user.id,
            liquid_id=liquid.id,
            amount=incoming_start_amount,
            from_who='Крулевщизна н/б'
        )
        incoming.save()

        new_incoming_liquid_id = new_liquid.id
        new_incoming_amount = 50

        response = self.app.put(f'/incoming/{incoming.id}', json={
            'liquid_id': new_incoming_liquid_id,
            'amount': new_incoming_amount,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/incoming/{incoming.id}?access_token={token.token}', json={
            'liquid_id': new_incoming_liquid_id,
            'amount': new_incoming_amount,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/incoming/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        incoming.deleted = True
        incoming.save()

        response = self.app.delete(f'/incoming/{incoming.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        incoming.deleted = False
        incoming.save()

        response = self.app.put(f'/incoming/{incoming.id}?access_token={token.token}', json={
            'liquid_id': 0,
            'amount': new_incoming_amount,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/incoming/{incoming.id}?access_token={token.token}', json={
            'amount': new_incoming_amount,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(liquid.balance, (liquid_start_balance - incoming_start_amount) + data['amount'])

        response = self.app.put(f'/incoming/{incoming.id}?access_token={token.token}', json={
            'liquid_id': new_incoming_liquid_id,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_incoming_liquid_id, data['liquid']['id'])
        self.assertEqual(liquid.balance, liquid_start_balance - incoming_start_amount)
        self.assertEqual(new_liquid.balance, new_liquid_start_balance + data['amount'])

    def test_coming_delete_page(self):
        user = User(**{
            'email': 'comingdelete@mail.ru',
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

        incoming = Incoming(
            user_id=user.id,
            liquid_id=liquid.id,
            amount=800,
            from_who='Крулевщизна н/б'
        )
        incoming.save()

        response = self.app.delete(f'/incoming/{incoming.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/incoming/{incoming.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/incoming/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        incoming.deleted = True
        incoming.save()

        response = self.app.delete(f'/incoming/{incoming.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        incoming.deleted = False
        incoming.save()

        response = self.app.delete(f'/incoming/{incoming.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
        self.assertEqual(liquid.balance, liquid_start_balance - incoming.amount)
