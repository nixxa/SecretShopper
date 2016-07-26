"""
This script runs the frontui application using a development server.
"""
import locale
from os import environ
from flask.ext.debugtoolbar import DebugToolbarExtension
from frontui.app import create_app

if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    app = create_app()
    HOST = environ.get('SERVER_HOST', 'localhost')
    MODE = environ.get('APP_MODE', 'DEBUG')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    if MODE == 'DEBUG':
        # register flask-debugtoolbar
        app.debug = True
        app.config['DEBUG'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        #app.dtb = DebugToolbarExtension(app)        
    app.run(HOST, PORT)
