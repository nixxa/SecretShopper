""" Auth decorator """
import functools
from flask import request, Response

def check_auth(username, password):
    """ Checks credentials """
    return username == 'admin' and password == 'secret'


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
