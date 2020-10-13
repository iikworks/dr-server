import os
from app.app import create_app
from dotenv import load_dotenv
load_dotenv()

app = create_app({
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL'),
    'API_TITLE': 'DieselReport API',
    'API_VERSION': '0.1',
    'OPENAPI_VERSION': '3.0.2',
})

if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.getenv('APP_HOST'),
        port=os.getenv('APP_PORT'),
    )
