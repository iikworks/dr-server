from functools import wraps
from flask import g, jsonify


def developer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.employee < 999:
            return jsonify({
                'error': 'access denied'
            }), 403

        return f(*args, **kwargs)
    return decorated_function
