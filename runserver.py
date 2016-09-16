"""
This script runs the frontui application using a development server.
"""
import locale
from os import environ
from frontui.app import create_app


if __name__ == '__main__':
    MODE = environ.get('APP_MODE', 'DEBUG')
    app = create_app(MODE)
    app.run('localhost', 5555)
