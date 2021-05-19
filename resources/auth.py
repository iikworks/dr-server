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

# Создание ресурса
auth = Blueprint('auth', 'auth', url_prefix='/auth')


@auth.route('/me')
class Me(MethodView):
    # Ресурс для показа информации авторизированного пользователя
    @auth.response(200, UserSchema)
    @auth_required
    def get(self):
        user_schema = UserSchema()

        return user_schema.dump(g.user)


@auth.route('/logout')
class Logout(MethodView):
    # Ресурс для выхода из текущего аккаунта (удаления активного токена)
    @auth_required
    def get(self):
        g.token.delete()

        return jsonify({
            'message': 'success logout'
        }), 200


@auth.route('/login')
class Login(MethodView):
    @auth.arguments(LoginQueryArgsSchema, location='json')
    @auth.response(200, AuthSuccessSchema)
    def post(self, data):
        # Ресурс для входа в аккаунт и создания нового токена
        # Необходимые данные: email, password
        # Возвращает: user_id, token, token_expires_in

        # Поиск пользователя по email в базе данных
        user = User.query.filter_by(email=data['email']).first()

        if user is None:
            return jsonify({'error': 'wrong email or password'}), 401

        # Проверка правильности ввода пароля
        if not user.check_password(data['password']):
            return jsonify({'error': 'wrong email or password'}), 401

        # Создание токена
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
    @auth.response(201, AuthSuccessSchema)
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
