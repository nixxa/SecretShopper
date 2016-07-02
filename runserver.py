"""
This script runs the frontui application using a development server.
"""
from os import environ
from frontui.app import create_app

if __name__ == '__main__':
    app = create_app()
    HOST = environ.get('SERVER_HOST', 'localhost')
    MODE = environ.get('APP_MODE', 'DEBUG')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    if MODE == 'DEBUG':
        app.debug = True
        app.config['DEBUG'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(HOST, PORT)
