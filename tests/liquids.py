import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.liquid import Liquid


class LiquidsTestCase(TestCase):
    def test_liquids_list_page(self):
        user = User(**{
            'email': 'liquidslist@mail.ru',
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

        response = self.app.get('/liquids/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(liquid.title, data['liquids'][0]['title'])

    def test_liquids_create_page(self):
        user = User(**{
            'email': 'logout@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/liquids/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/liquids/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        liquid_prefix = 'Масло'
        liquid_title = 'М10-Г2'
        liquid_balance = 800.50
        liquid_unit = 'л'

        test_cases = {
            'missing_title': {
                'data': {
                    'prefix': liquid_prefix,
                    'balance': liquid_balance,
                    'unit': liquid_unit,
                },
                'status_code': 422
            }, 'wrong_balance': {
                'data': {
                    'prefix': liquid_prefix,
                    'title': liquid_title,
                    'balance': '0 22',
                    'unit': liquid_unit,
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'prefix': liquid_prefix,
                    'title': liquid_title,
                    'balance': liquid_balance,
                    'unit': liquid_unit,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/liquids/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(liquid_prefix, data['prefix'])
                self.assertEqual(liquid_title, data['title'])
                self.assertEqual(liquid_balance, data['balance'])
                self.assertEqual(liquid_unit, data['unit'])

    def test_liquid_detail_page(self):
        user = User(**{
            'email': 'liquiddetail@mail.ru',
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

        response = self.app.get(f'/liquids/0')
        self.assertEqual(response.status_code, 404)

        liquid.deleted = True
        liquid.save()

        response = self.app.get(f'/liquids/{liquid.id}')
        self.assertEqual(response.status_code, 404)

        liquid.deleted = False
        liquid.save()

        response = self.app.get(f'/liquids/{liquid.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(liquid.title, data['title'])

    def test_liquid_edit_page(self):
        user = User(**{
            'email': 'liquiddetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=888.50
        )
        liquid.save()

        new_liquid_prefix = 'Масло'
        new_liquid_title = 'М10-Г2'
        new_liquid_balance = 800.50

        response = self.app.put(f'/liquids/{liquid.id}', json={
            'prefix': new_liquid_prefix,
            'title': new_liquid_title,
            'balance': new_liquid_balance,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/liquids/{liquid.id}?access_token={token.token}', json={
            'prefix': new_liquid_prefix,
            'title': new_liquid_title,
            'balance': new_liquid_balance,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        liquid.deleted = True
        liquid.save()

        response = self.app.delete(f'/liquids/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        response = self.app.put(f'/liquids/{liquid.id}?access_token={token.token}', json={
            'prefix': new_liquid_prefix,
            'title': new_liquid_title,
            'balance': new_liquid_balance,
        })
        self.assertEqual(response.status_code, 404)

        liquid.deleted = False
        liquid.save()

        response = self.app.put(f'/liquids/{liquid.id}?access_token={token.token}', json={
            'prefix': new_liquid_prefix,
            'title': new_liquid_title,
            'balance': '0 22',
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/liquids/{liquid.id}?access_token={token.token}', json={
            'prefix': new_liquid_prefix,
            'title': new_liquid_title,
            'balance': new_liquid_balance,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_liquid_prefix, data['prefix'])
        self.assertEqual(new_liquid_title, data['title'])
        self.assertEqual(new_liquid_balance, data['balance'])

        new_liquid_prefix = 'Oil'

        response = self.app.put(f'/liquids/{liquid.id}?access_token={token.token}', json={
            'prefix': new_liquid_prefix,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_liquid_prefix, data['prefix'])

    def test_liquid_delete_page(self):
        user = User(**{
            'email': 'liquiddetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=888.50
        )
        liquid.save()

        response = self.app.delete(f'/liquids/{liquid.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/liquids/{liquid.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/liquids/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        liquid.deleted = True
        liquid.save()

        response = self.app.delete(f'/liquids/{liquid.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        liquid.deleted = False
        liquid.save()

        response = self.app.delete(f'/liquids/{liquid.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
