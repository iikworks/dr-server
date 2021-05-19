import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from resources import load_resources
from models import db
from app.cli import register_commands

migrate = Migrate(compare_type=True)


def create_app(config):
    # Создание приложения
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    )

    # Добавление необходимых настроек из объекта config
    app.app_context().push()
    app.config.update(config)

    # Установка необходимых модулей, регистрация путей и CLI
    setup_app(app)
    register_commands(app)
    return app


def setup_app(app):
    # Защита CORS
    CORS(app)

    # Настройка базы данных
    db.init_app(app)

    # Настройка миграций
    migrate.init_app(app, db)

    # Настройка ресурсов (путей)
    load_resources(app)
