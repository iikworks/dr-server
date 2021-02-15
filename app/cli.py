import click
from models.user import User


def register_commands(app):
    @app.cli.command('create-dev-user')
    def create_dev_user():
        email = click.prompt('Введите адрес электронной почты', type=str)
        first_name = click.prompt('Введите имя', type=str)
        last_name = click.prompt('Введите фамилию', type=str)

        password = ''
        while(password == ''):
            temp_password = click.prompt('Введите пароль', type=str, hide_input=True)
            repeat_password = click.prompt('Повторите пароль', type=str, hide_input=True)

            if temp_password == repeat_password:
                password = temp_password
            else:
                print('Неверный пароль. Повторите ещё раз.')
        
        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'employee': 999
        }

        user = User(**data)
        user.save()

        print('Пользователь {} (ID: {}), {} {} успешно создан.'.format(user.email, user.id, user.first_name, user.last_name))
