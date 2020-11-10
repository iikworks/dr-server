from flask_smorest import Api
from .auth import auth
from .liquids import liquids
from .vehicles import vehicles
from .workers import workers


def load_resources(app):
    api = Api(app)

    api.register_blueprint(auth)
    api.register_blueprint(liquids)
    api.register_blueprint(vehicles)
    api.register_blueprint(workers)

    return api
