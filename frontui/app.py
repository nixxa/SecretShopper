""" Creat and init application """
import logging
import os
from flask import Flask
from frontui import BASE_DIR
from frontui.views.public import public_ui
from frontui.views.restricted import restricted_ui


def create_app(app_mode='DEBUG'):
    """ Create application, register blueprints, etc """
    if app_mode == '':
        app_mode = os.environ.get('APP_MODE', 'DEBUG')
    # create an application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'\x88~\x17h\xdc;,\x9f\x1do\x98\xcd\xaf|\x1c\x19\xec\xcf\xb1\x12\xd4\x8b\xcdQ'
    # set logging
    app.debug_log_format = '%(asctime)s %(levelname)s %(message)s'
    app.logger.setLevel(logging.DEBUG)
    if app_mode == 'DEBUG':
        app.debug = True
        app.config['DEBUG'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s'
        )
    if app_mode == 'PROD':
        logging.basicConfig(
            filename='app.log',
            format='%(asctime)s %(levelname)s %(message)s',
            level=logging.DEBUG)
    # register blueprints
    app.register_blueprint(public_ui)
    app.register_blueprint(restricted_ui)
    # register jinja exts
    app.add_template_filter(f=points, name='points')
    # configure uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    # app started
    logging.info('Application started in %s mode', app_mode)
    return app


def points(answer, question):
    return str(question.cost) if answer == 'yes' else '0' if answer == 'no' else ''