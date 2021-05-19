from flask_smorest import Api
from .auth import auth
from .liquids import liquids
from .vehicles import vehicles
from .workers import workers
from .incoming import incoming
from .expenses import expenses
from .homestats import homestats
from .invites import invites
from .posts import posts


def load_resources(app):
    # Регистрация всех ресурсов (путей)

    api = Api(app)

    api.register_blueprint(auth)
    api.register_blueprint(liquids)
    api.register_blueprint(vehicles)
    api.register_blueprint(workers)
    api.register_blueprint(incoming)
    api.register_blueprint(expenses)
    api.register_blueprint(homestats)
    api.register_blueprint(invites)
    api.register_blueprint(posts)

    return api
