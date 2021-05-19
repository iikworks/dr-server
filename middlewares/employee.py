from functools import wraps
from flask import g, jsonify


def developer_required(f):
    # Промежуточный обработчик для страниц, доступ к которым имеет только разработчик
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Проверка уровня доступа
        if g.user.employee < 999:
            return jsonify({
                'error': 'access denied'
            }), 403

        return f(*args, **kwargs)
    return decorated_function
