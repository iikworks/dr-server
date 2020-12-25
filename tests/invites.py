import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.vehicle import Vehicle
from models.invite import Invite


class InvitesTestCase(TestCase):
    def test_invites_list_page(self):
        invite = Invite()
        invite.save()

        response = self.app.get('/invites/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(invite.code, data['invites'][0]['code'])

    def test_invites_create_page(self):
        user = User(**{
            'email': 'invitescreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/invites/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/invites/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.post(f'/invites/?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

    def test_vehicle_detail_page(self):
        invite = Invite()
        invite.save()

        response = self.app.get(f'/invites/0')
        self.assertEqual(response.status_code, 404)

        response = self.app.get(f'/invites/{invite.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(invite.code, data['code'])

    def test_invite_edit_page(self):
        user = User(**{
            'email': 'inviteedit@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        invite = Invite()
        invite.save()

        response = self.app.put(f'/invites/{invite.id}', json={
            'used': True,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/invites/{invite.id}?access_token={token.token}', json={
            'used': True,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.put(f'/invites/{invite.id}?access_token={token.token}', json={
            'used': True,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(True, data['used'])
