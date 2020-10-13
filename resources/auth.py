from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.user import LoginQueryArgsSchema, SignUpQueryArgsSchema, UserSchema
from models.user import User

auth = Blueprint('auth', 'auth', url_prefix='/auth')


@auth.route('/login')
class Login(MethodView):
    @auth.arguments(LoginQueryArgsSchema, location='json')
    @auth.response(UserSchema, code=200)
    def post(self, data):
        pass


@auth.route('/signup')
class SignUp(MethodView):
    @auth.arguments(SignUpQueryArgsSchema, location='json')
    @auth.response(UserSchema, code=201)
    def post(self, data):
        del data['password_repeat']

        user = User(**data)
        user.save()

        return user
