import unittest
from main import app
from models import db


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_sign_up_page(self):
        db.drop_all()
        db.create_all()

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
                    'email': 'test@mail.ru',
                    'first_name': 'John223',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 422
            }, 'wrong_last_name': {
                'data': {
                    'email': 'test@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device gg',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 422
            }, 'wrong_password': {
                'data': {
                    'email': 'test@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '1111',
                    'password_repeat': '1111',
                },
                'status_code': 422
            }, 'wrong_password_repeat': {
                'data': {
                    'email': 'test@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '1111',
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'email': 'test@mail.ru',
                    'first_name': 'John',
                    'last_name': 'Device',
                    'password': '111111',
                    'password_repeat': '111111',
                },
                'status_code': 201
            }, 'email_used': {
                'data': {
                    'email': 'test@mail.ru',
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

