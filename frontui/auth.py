""" Auth decorator """
import functools
from flask import request, Response, session
from frontui.data_provider import DataProvider
from frontui.linq import first_or_default


def check_auth(username, password):
    """ Checks credentials """
    database = DataProvider()
    current_user = first_or_default(database.users, lambda x: x.username == username)
    if current_user is None:
        return False
    if current_user.password != password:
        return False
    session['user_name'] = current_user.username
    session['user_role'] = current_user.rolename
    return True

def authenticate():
    """ Sends 401 response """
    return Response(
        'Требуется авторизация\n'
        'Укажите имя пользователя и пароль',
        401,
        {'WWW-Authenticate': 'Basic realm="SecretShopper"'}
    )

def authorize(route):
    """ Auth decorator """
    @functools.wraps(route)
    def decorated(*args, **kwargs):
        """ Decorate request """
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return route(*args, **kwargs)
    return decorated
