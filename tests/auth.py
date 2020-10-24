from tests.testcase import TestCase
from models.user import User
from models.token import Token


class AuthTestCase(TestCase):
    def test_me_page(self):
        user = User(**{
            'email': 'me@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.get('/auth/me')
        self.assertEqual(response.status_code, 401)

        response = self.app.get(f'/auth/me?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        self.assertIn(f'"id":{user.id}', response.data.decode('UTF-8'))

    def test_logout_page(self):
        user = User(**{
            'email': 'logout@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.get('/auth/logout')
        self.assertEqual(response.status_code, 401)

        response = self.app.get(f'/auth/logout?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(token.deleted, True)

    def test_login_page(self):
        test_email = 'login@mail.ru'
        test_password = '111111'

        user = User(**{
            'email': test_email,
            'first_name': 'Test',
            'last_name': 'User',
            'password': test_password,
        })
        user.save()

        test_cases = {
            'wrong_email': {
                'data': {
                    'email': 'wrong@mail.ru',
                    'password': test_password,
                },
                'status_code': 401
            }, 'wrong_password': {
                'data': {
                    'email': test_email,
                    'password': 'wrong',
                },
                'status_code': 401
            }, 'success': {
                'data': {
                    'email': test_email,
                    'password': test_password,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post('/auth/login', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                self.assertIn(f'"user_id":{user.id}', response.data.decode('UTF-8'))
                self.assertIn('token', response.data.decode('UTF-8'))
                self.assertIn('token_expires_in', response.data.decode('UTF-8'))

    def test_sign_up_page(self):
        test_cases = {
            'wrong_email': {
                'data': {
                    'email': 'wrong',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 422
            }, 'wrong_first_name': {
                'data': {
                    'email': 'signup@mail.ru',
                    'first_name': 'John223',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 422
            }, 'wrong_last_name': {
                'data': {
                    'email': 'signup@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device gg',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 422
            }, 'wrong_password': {
                'data': {
                    'email': 'signup@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '1111',
                    'password_repeat': '1111',
                },
                'status_code': 422
            }, 'wrong_password_repeat': {
                'data': {
                    'email': 'signup@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '1111',
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'email': 'signup@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 201
            }, 'email_used': {
                'data': {
                    'email': 'signup@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 422
            },
        }

        for name, test_case in test_cases.items():
            response = self.app.post('/auth/signup', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                self.assertIn('user_id', response.data.decode('UTF-8'))
                self.assertIn('token', response.data.decode('UTF-8'))
                self.assertIn('token_expires_in', response.data.decode('UTF-8'))
