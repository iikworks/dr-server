from functools import wraps
from flask import g, jsonify, request
from models.token import Token


def auth_required(f):
    # Промежуточный обработчик для страниц, доступ к которым имеет только авторизированный
    #    пользователь

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Поиск в аргументах запроса ключа access_token
        if 'access_token' not in request.args:
            return jsonify({
                'error': 'auth required'
            }), 401

        # Поиск найденного токена в базе данных
        token = Token.get_by_token(request.args.get('access_token'))
        if token is None:
            return jsonify({
                'error': 'auth required'
            }), 401

        # Проверка, не истек ли срок действия токена
        if not token.is_token_has_no_expires():
            return jsonify({
                'error': 'auth required'
            }), 401

        # Добавление токена и владельца токена в запрос
        g.token = token
        g.user = token.user

        return f(*args, **kwargs)
    return decorated_function
