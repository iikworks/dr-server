import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from resources import load_resources
from models import db

migrate = Migrate(compare_type=True)


def create_app(config):
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    )

    app.app_context().push()
    app.config.update(config)

    setup_app(app)
    return app


def setup_app(app):
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    load_resources(app)
