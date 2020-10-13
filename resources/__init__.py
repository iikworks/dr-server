from flask_smorest import Api
from .auth import auth


def load_resources(app):
    api = Api(app)

    api.register_blueprint(auth)

    return api
