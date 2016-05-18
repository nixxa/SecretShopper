"""
This script runs the frontui application using a development server.
"""

from os import environ
from frontui import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    MODE = environ.get('APP_MODE', 'DEBUG')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    if MODE == 'DEBUG':
        app.debug = True
    app.run(HOST, PORT)
