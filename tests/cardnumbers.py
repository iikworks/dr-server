import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.cardnumber import CardNumber


class CardNumbersTestCase(TestCase):
    def test_cardnumbers_list_page(self):
        user = User(**{
            'email': 'cardnumberslist@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        cardnumber = CardNumber(
            user_id=user.id,
            title='ГСМ Трактора',
        )
        cardnumber.save()

        response = self.app.get('/cardnumbers/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(cardnumber.title, data['cardnumbers'][0]['title'])

    def test_cardnumbers_create_page(self):
        user = User(**{
            'email': 'cardnumberscreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/cardnumbers/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/cardnumbers/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        cardnumbers_title = 'ГСМ Трактора'

        test_cases = {
            'missing_title': {
                'data': {
                    
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'title': cardnumbers_title,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/cardnumbers/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(cardnumbers_title, data['title'])

    def test_cardnumbers_edit_page(self):
        user = User(**{
            'email': 'cardnumbersedit@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        cardnumber = CardNumber(
            user_id=user.id,
            title='ГСМ Трактора',
        )
        cardnumber.save()

        new_cardnumber_title = 'ГСМ Автомобили'
        new_cardnumber_number = 5

        response = self.app.put(f'/cardnumbers/{cardnumber.id}', json={
            'title': new_cardnumber_title,
            'number': new_cardnumber_number,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/cardnumbers/{cardnumber.id}?access_token={token.token}', json={
            'title': new_cardnumber_title,
            'number': new_cardnumber_number,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        cardnumber.deleted = True
        cardnumber.save()

        response = self.app.delete(f'/cardnumbers/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        response = self.app.put(f'/cardnumbers/{cardnumber.id}?access_token={token.token}', json={
            'title': new_cardnumber_title,
            'number': new_cardnumber_number,
        })
        self.assertEqual(response.status_code, 404)

        cardnumber.deleted = False
        cardnumber.save()

        response = self.app.put(f'/cardnumbers/{cardnumber.id}?access_token={token.token}', json={
            'title': '',
            'number': new_cardnumber_number,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/cardnumbers/{cardnumber.id}?access_token={token.token}', json={
            'title': new_cardnumber_title,
            'number': new_cardnumber_number,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_cardnumber_title, data['title'])
        self.assertEqual(new_cardnumber_number, data['number'])

    def test_cardnumbers_delete_page(self):
        user = User(**{
            'email': 'cardnumbersdelete@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        cardnumber = CardNumber(
            user_id=user.id,
            title='ГСМ Трактора',
        )
        cardnumber.save()

        response = self.app.delete(f'/cardnumbers/{cardnumber.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/cardnumbers/{cardnumber.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/cardnumbers/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        cardnumber.deleted = True
        cardnumber.save()

        response = self.app.delete(f'/cardnumbers/{cardnumber.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        cardnumber.deleted = False
        cardnumber.save()

        response = self.app.delete(f'/cardnumbers/{cardnumber.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
