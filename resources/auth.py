from flask import jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from models.user import User
from models.token import Token
from models.invite import Invite
from app.helpers import to_fixed
from middlewares import auth_required
from schemas.user import (
    UserSchema,
    LoginQueryArgsSchema,
    SignUpQueryArgsSchema,
    AuthSuccessSchema
)

auth = Blueprint('auth', 'auth', url_prefix='/auth')


@auth.route('/me')
class Me(MethodView):
    @auth.response(UserSchema, code=200)
    @auth_required
    def get(self):
        user_schema = UserSchema()

        return user_schema.dump(g.user)


@auth.route('/logout')
class Logout(MethodView):
    @auth_required
    def get(self):
        g.token.delete()

        return jsonify({
            'message': 'success logout'
        }), 200


@auth.route('/login')
class Login(MethodView):
    @auth.arguments(LoginQueryArgsSchema, location='json')
    @auth.response(AuthSuccessSchema, code=200)
    def post(self, data):
        user = User.query.filter_by(email=data['email']).first()

        if user is None:
            return jsonify({'error': 'wrong email or password'}), 401

        if not user.check_password(data['password']):
            return jsonify({'error': 'wrong email or password'}), 401

        token = Token(user.id)
        token.save()

        auth_success_schema = AuthSuccessSchema()

        return auth_success_schema.dump({
            'user_id': user.id,
            'token': token.token,
            'token_expires_in': to_fixed(token.expires_in.timestamp())
        })


@auth.route('/signup')
class SignUp(MethodView):
    @auth.arguments(SignUpQueryArgsSchema, location='json')
    @auth.response(AuthSuccessSchema, code=201)
    def post(self, data):
        del data['password_repeat']

        invite = data['invite']
        del data['invite']

        user = User(**data)
        user.save()

        invite = Invite.query.filter_by(code=invite, used=False).first()
        invite.set_used(user.id)
        invite.save()

        token = Token(user.id)
        token.save()

        auth_success_schema = AuthSuccessSchema()

        return auth_success_schema.dump({
            'user_id': user.id,
            'token': token.token,
            'token_expires_in': to_fixed(token.expires_in.timestamp())
        })
