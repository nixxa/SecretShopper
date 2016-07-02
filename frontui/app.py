""" Creat and init application """
import logging
from flask import Flask
from flask.ext.mobility import Mobility
from frontui.views import ui


def create_app():
    """ Create application, register blueprints, etc """
    # create an application
    app = Flask(__name__)
    # set logging
    app.debug_log_format = '%(asctime)s %(levelname)s %(message)s'
    app.logger.setLevel(logging.DEBUG)
    # register blueprints
    app.register_blueprint(ui)
    # register mobility
    Mobility(app)
    # register jinja exts
    app.jinja_env.tests['equalto'] = lambda x, y: x == y
    return app
