import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.liquid import Liquid
from models.homestats import HomeStats


class HomeStatsTestCase(TestCase):
    def test_homestats_list_page(self):
        user = User(**{
            'email': 'homestatslist@mail.ru',
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

        homestat = HomeStats(
            user_id=user.id,
            liquid_id=liquid.id,
            title='Остаток дизельного топлива',
            place=1,
            position=1,
            stat_type='exp',
        )
        homestat.save()

        response = self.app.get('/homestats/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(homestat.liquid.id, data['homestats'][0]['liquid']['id'])
        self.assertEqual(homestat.title, data['homestats'][0]['title'])
        self.assertEqual(homestat.place, data['homestats'][0]['place'])
        self.assertEqual(homestat.position, data['homestats'][0]['position'])
        self.assertEqual(homestat.type, data['homestats'][0]['type'])

    def test_homestats_create_page(self):
        user = User(**{
            'email': 'homestatscreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/homestats/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/homestats/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        liquid = Liquid(
            user_id=user.id,
            title='Дизельное топливо',
            balance=885.50
        )
        liquid.save()

        homestat_liquid_id = liquid.id
        homestat_title = 'Остаток дизельного топлива'
        homestat_place = 1
        homestat_position = 3
        homestat_type = 'exp'

        test_cases = {
            'missing_liquid_id': {
                'data': {
                    'title': homestat_title,
                    'place': homestat_place,
                    'position': homestat_position,
                    'type': homestat_type,
                },
                'status_code': 422
            }, 'missing_title': {
                'data': {
                    'liquid_id': homestat_liquid_id,
                    'place': homestat_place,
                    'position': homestat_position,
                    'type': homestat_type,
                },
                'status_code': 422
            }, 'wrong_type': {
                'data': {
                    'liquid_id': homestat_liquid_id,
                    'title': homestat_title,
                    'place': homestat_place,
                    'position': homestat_position,
                    'type': 'wrong',
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'liquid_id': homestat_liquid_id,
                    'title': homestat_title,
                    'place': homestat_place,
                    'position': homestat_position,
                    'type': homestat_type,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/homestats/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(homestat_liquid_id, data['liquid']['id'])
                self.assertEqual(homestat_title, data['title'])
                self.assertEqual(homestat_place, data['place'])
                self.assertEqual(homestat_position, data['position'])
                self.assertEqual(homestat_type, data['type'])

    def test_homestat_detail_page(self):
        user = User(**{
            'email': 'homestatdetail@mail.ru',
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

        homestat = HomeStats(
            user_id=user.id,
            liquid_id=liquid.id,
            title='Остаток дизельного топлива',
            place=1,
            position=1,
            stat_type='exp',
        )
        homestat.save()

        response = self.app.get(f'/homestats/0')
        self.assertEqual(response.status_code, 404)

        homestat.deleted = True
        homestat.save()

        response = self.app.get(f'/homestats/{homestat.id}')
        self.assertEqual(response.status_code, 404)

        homestat.deleted = False
        homestat.save()

        response = self.app.get(f'/homestats/{homestat.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(homestat.liquid.id, data['liquid']['id'])
        self.assertEqual(homestat.title, data['title'])
        self.assertEqual(homestat.place, data['place'])
        self.assertEqual(homestat.position, data['position'])
        self.assertEqual(homestat.type, data['type'])

    def test_homestat_edit_page(self):
        user = User(**{
            'email': 'homestatedit@mail.ru',
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

        new_liquid = Liquid(
            user_id=user.id,
            title='Масло М10-Г2',
            balance=8.50
        )
        new_liquid.save()

        homestat = HomeStats(
            user_id=user.id,
            liquid_id=liquid.id,
            title='Остаток дизельного топлива',
            place=1,
            position=1,
            stat_type='exp',
        )
        homestat.save()

        new_homestat_liquid_id = new_liquid.id

        response = self.app.put(f'/homestats/{homestat.id}', json={
            'liquid_id': new_homestat_liquid_id,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/homestats/{homestat.id}?access_token={token.token}', json={
            'liquid_id': new_homestat_liquid_id,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/homestats/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        homestat.deleted = True
        homestat.save()

        response = self.app.delete(f'/homestats/{homestat.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        homestat.deleted = False
        homestat.save()

        response = self.app.put(f'/homestats/{homestat.id}?access_token={token.token}', json={
            'liquid_id': 0
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/homestats/{homestat.id}?access_token={token.token}', json={
            'liquid_id': new_homestat_liquid_id,
            'type': 'inc',
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_homestat_liquid_id, data['liquid']['id'])
        self.assertEqual('inc', data['type'])

    def test_homestat_delete_page(self):
        user = User(**{
            'email': 'homestatdelete@mail.ru',
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

        homestat = HomeStats(
            user_id=user.id,
            liquid_id=liquid.id,
            title='Остаток дизельного топлива',
            place=1,
            position=1,
            stat_type='exp',
        )
        homestat.save()

        response = self.app.delete(f'/homestats/{homestat.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/homestats/{homestat.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/homestats/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        homestat.deleted = True
        homestat.save()

        response = self.app.delete(f'/homestats/{homestat.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        homestat.deleted = False
        homestat.save()

        response = self.app.delete(f'/homestats/{homestat.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
