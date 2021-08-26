import json
from tests.testcase import TestCase
from models.user import User


class UsersTestCase(TestCase):
    def test_users_list_page(self):
        user = User(**{
            'email': 'userslist@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        response = self.app.get('/users/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(user.first_name, data['users'][0]['first_name'])
        self.assertEqual(user.last_name, data['users'][0]['last_name'])
        self.assertEqual(user.employee, data['users'][0]['employee'])

    def test_user_detail_page(self):
        user = User(**{
            'email': 'userdetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        response = self.app.get(f'/users/0')
        self.assertEqual(response.status_code, 404)

        user.deleted = True
        user.save()

        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 404)

        user.deleted = False
        user.save()

        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.employee, data['employee'])
