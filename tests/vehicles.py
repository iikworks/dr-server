import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.vehicle import Vehicle


class VehiclesTestCase(TestCase):
    def test_vehicles_list_page(self):
        user = User(**{
            'email': 'vehicleslist@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            brand='МАЗ',
            model='555102',
            government_number=11
        )
        vehicle.save()

        response = self.app.get('/vehicles/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(vehicle.model, data['vehicles'][0]['model'])

    def test_vehicles_create_page(self):
        user = User(**{
            'email': 'vehiclescreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/vehicles/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/vehicles/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        vehicle_type = 'harvester'
        vehicle_model = 'КЗС-1218'
        vehicle_government_number = 339

        test_cases = {
            'missing_title': {
                'data': {
                    'model': vehicle_model,
                    'government_number': vehicle_government_number,
                },
                'status_code': 422
            }, 'wrong_type': {
                'data': {
                    'type': 'wrong',
                    'model': vehicle_model,
                    'government_number': vehicle_government_number,
                },
                'status_code': 422
            }, 'wrong_government_number': {
                'data': {
                    'type': vehicle_type,
                    'model': vehicle_model,
                    'government_number': 99999,
                },
                'status_code': 422
            }, 'success': {
                'data': {
                    'type': vehicle_type,
                    'model': vehicle_model,
                    'government_number': vehicle_government_number,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/vehicles/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(vehicle_type, data['type'])
                self.assertEqual(vehicle_model, data['model'])
                self.assertEqual(vehicle_government_number, data['government_number'])

    def test_vehicle_detail_page(self):
        user = User(**{
            'email': 'vehicledetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            brand='МАЗ',
            model='555102',
            government_number=11
        )
        vehicle.save()

        response = self.app.get(f'/vehicles/0')
        self.assertEqual(response.status_code, 404)

        vehicle.deleted = True
        vehicle.save()

        response = self.app.get(f'/vehicles/{vehicle.id}')
        self.assertEqual(response.status_code, 404)

        vehicle.deleted = False
        vehicle.save()

        response = self.app.get(f'/vehicles/{vehicle.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(vehicle.model, data['model'])

    def test_vehicle_edit_page(self):
        user = User(**{
            'email': 'vehicleedit@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            brand='МАЗ',
            model='555102',
            government_number=11
        )
        vehicle.save()

        new_vehicle_type = 'tractor'
        new_vehicle_brand = 'МТЗ'
        new_vehicle_model = '3022'
        new_vehicle_government_number = 8197

        response = self.app.put(f'/vehicles/{vehicle.id}', json={
            'type': new_vehicle_type,
            'brand': new_vehicle_brand,
            'model': new_vehicle_model,
            'government_number': new_vehicle_government_number,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/vehicles/{vehicle.id}?access_token={token.token}', json={
            'type': new_vehicle_type,
            'brand': new_vehicle_brand,
            'model': new_vehicle_model,
            'government_number': new_vehicle_government_number,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        vehicle.deleted = True
        vehicle.save()

        response = self.app.delete(f'/vehicles/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        response = self.app.put(f'/vehicles/{vehicle.id}?access_token={token.token}', json={
            'type': new_vehicle_type,
            'brand': new_vehicle_brand,
            'model': new_vehicle_model,
            'government_number': new_vehicle_government_number,
        })
        self.assertEqual(response.status_code, 404)

        vehicle.deleted = False
        vehicle.save()

        response = self.app.put(f'/vehicles/{vehicle.id}?access_token={token.token}', json={
            'type': 'wrong_type',
            'brand': new_vehicle_brand,
            'model': new_vehicle_model,
            'government_number': new_vehicle_government_number,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/vehicles/{vehicle.id}?access_token={token.token}', json={
            'type': new_vehicle_type,
            'brand': new_vehicle_brand,
            'model': new_vehicle_model,
            'government_number': 99999,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/vehicles/{vehicle.id}?access_token={token.token}', json={
            'type': new_vehicle_type,
            'brand': new_vehicle_brand,
            'model': new_vehicle_model,
            'government_number': new_vehicle_government_number,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_vehicle_type, data['type'])
        self.assertEqual(new_vehicle_brand, data['brand'])
        self.assertEqual(new_vehicle_model, data['model'])
        self.assertEqual(new_vehicle_government_number, data['government_number'])

    def test_vehicle_delete_page(self):
        user = User(**{
            'email': 'vehicledelete@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        vehicle = Vehicle(
            user_id=user.id,
            v_type='car',
            brand='МАЗ',
            model='555102',
            government_number=11
        )
        vehicle.save()

        response = self.app.delete(f'/vehicles/{vehicle.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/vehicles/{vehicle.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/vehicles/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        vehicle.deleted = True
        vehicle.save()

        response = self.app.delete(f'/vehicles/{vehicle.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        vehicle.deleted = False
        vehicle.save()

        response = self.app.delete(f'/vehicles/{vehicle.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
