from functools import wraps
from flask import g, jsonify, request
from models.token import Token


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in request.args:
            return jsonify({
                'error': 'auth required'
            }), 401

        token = Token.get_by_token(request.args.get('access_token'))
        if token is None:
            return jsonify({
                'error': 'auth required'
            }), 401

        if not token.is_token_has_no_expires():
            return jsonify({
                'error': 'auth required'
            }), 401

        g.token = token
        g.user = token.user

        return f(*args, **kwargs)
    return decorated_function
