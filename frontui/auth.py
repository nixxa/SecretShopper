""" Auth decorator """
import functools
from flask import request, Response, session
from frontui.data_provider import DataProvider

USERS = [ 
    ('admin', 'secret', 'internal'),
    ('anna', 'aprelevka', 'internal'),
    ('valar', 'valar', 'external')
]

def check_auth(username, password):
    """ Checks credentials """
    completed = False
    for item in USERS:
        checked = item[0] == username and item[1] == password
        if checked:
            session['user_name'] = item[0]
            session['user_role'] = item[2]
        completed = completed or checked
    return completed


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
