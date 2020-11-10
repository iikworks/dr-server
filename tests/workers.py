import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.worker import Worker


class WorkersTestCase(TestCase):
    def test_workers_list_page(self):
        user = User(**{
            'email': 'workerslist@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        response = self.app.get('/workers/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(worker.first_name, data['workers'][0]['first_name'])
        self.assertEqual(worker.last_name, data['workers'][0]['last_name'])
        self.assertEqual(worker.patronymic, data['workers'][0]['patronymic'])

    def test_workers_create_page(self):
        user = User(**{
            'email': 'workerscreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/workers/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/workers/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        worker_first_name = 'Петр'
        worker_last_name = 'Петров'
        worker_patronymic = 'Петрович'

        test_cases = {
            'missing_first_name': {
                'data': {
                    'last_name': worker_last_name,
                    'patronymic': worker_patronymic,
                },
                'status_code': 422
            }, 'missing_last_name': {
                'data': {
                    'first_name': worker_first_name,
                    'patronymic': worker_patronymic,
                },
                'status_code': 422
            },  'success': {
                'data': {
                    'first_name': worker_first_name,
                    'last_name': worker_last_name,
                    'patronymic': worker_patronymic,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/workers/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(worker_first_name, data['first_name'])
                self.assertEqual(worker_last_name, data['last_name'])
                self.assertEqual(worker_patronymic, data['patronymic'])

    def test_worker_detail_page(self):
        user = User(**{
            'email': 'workerdetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        response = self.app.get(f'/workers/0')
        self.assertEqual(response.status_code, 404)

        worker.deleted = True
        worker.save()

        response = self.app.get(f'/workers/{worker.id}')
        self.assertEqual(response.status_code, 404)

        worker.deleted = False
        worker.save()

        response = self.app.get(f'/workers/{worker.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(worker.first_name, data['first_name'])
        self.assertEqual(worker.last_name, data['last_name'])
        self.assertEqual(worker.patronymic, data['patronymic'])

    def test_worker_edit_page(self):
        user = User(**{
            'email': 'workeredit@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        new_worker_first_name = 'Максим'
        new_worker_last_name = 'Максимов'
        new_worker_patronymic = 'Максимович'

        response = self.app.put(f'/workers/{worker.id}', json={
            'first_name': new_worker_first_name,
            'last_name': new_worker_last_name,
            'patronymic': new_worker_patronymic,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/workers/{worker.id}?access_token={token.token}', json={
            'first_name': new_worker_first_name,
            'last_name': new_worker_last_name,
            'patronymic': new_worker_patronymic,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        worker.deleted = True
        worker.save()

        response = self.app.delete(f'/workers/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        response = self.app.put(f'/workers/{worker.id}?access_token={token.token}', json={
            'first_name': new_worker_first_name,
            'last_name': new_worker_last_name,
            'patronymic': new_worker_patronymic,
        })
        self.assertEqual(response.status_code, 404)

        worker.deleted = False
        worker.save()

        response = self.app.put(f'/workers/{worker.id}?access_token={token.token}', json={
            'first_name': '',
            'last_name': new_worker_last_name,
            'patronymic': new_worker_patronymic,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/workers/{worker.id}?access_token={token.token}', json={
            'first_name': new_worker_first_name,
            'last_name': new_worker_last_name,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_worker_first_name, data['first_name'])
        self.assertEqual(new_worker_last_name, data['last_name'])

    def test_worker_delete_page(self):
        user = User(**{
            'email': 'workerdelete@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        worker = Worker(
            user_id=user.id,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович'
        )
        worker.save()

        response = self.app.delete(f'/workers/{worker.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/workers/{worker.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/workers/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        worker.deleted = True
        worker.save()

        response = self.app.delete(f'/workers/{worker.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        worker.deleted = False
        worker.save()

        response = self.app.delete(f'/workers/{worker.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
