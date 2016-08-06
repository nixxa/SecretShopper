""" Creat and init application """
import logging
from flask import Flask
from flask.ext.mobility import Mobility
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
    # register blueprints
    app.register_blueprint(ui)
    # register mobility
    Mobility(app)
    # register jinja exts
    app.jinja_env.tests['equalto'] = \
        lambda x, y: x == y
    app.jinja_env.filters['points'] = \
        lambda answer, question: str(question.cost) if answer == 'yes' else '0' if answer == 'no' else ''
    # configure uploads
    app.config['UPLOAD_FOLDER'] = './frontui/uploads'
    return app
