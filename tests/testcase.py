import unittest
from app.app import create_app
from models import db

app = create_app({
    'API_TITLE': 'DieselReport Test',
    'API_VERSION': 't.t',
    'OPENAPI_VERSION': '3.0.2',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()
