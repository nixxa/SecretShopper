""" Creat and init application """
import logging
import os
from flask import Flask
from frontui.views import ui


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
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s'
        )
    if app_mode == 'PROD':
        #create_rotating_log(app, 'app.log')
        logging.basicConfig(
            filename='app.log',
            format='%(asctime)s %(levelname)s %(message)s',
            level=logging.DEBUG)
    # register blueprints
    app.register_blueprint(ui)
    # register jinja exts
    app.jinja_env.tests['equalto'] = \
        lambda x, y: x == y
    app.jinja_env.filters['points'] = \
        lambda answer, question: str(question.cost) if answer == 'yes' else '0' if answer == 'no' else ''
    # configure uploads
    app.config['UPLOAD_FOLDER'] = './frontui/uploads'
    # configure sendgrid options
    app.config['SENDGRID_APIKEY'] = os.environ.get('SENDGRID_APIKEY', '')
    app.config['SENDGRID_USERNAME'] = os.environ.get('SENDGRID_USERNAME', '')
    app.config['SENDGRID_PASSWORD'] = os.environ.get('SENDGRID_PASSWORD', '')
    return app
