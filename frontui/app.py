""" Creat and init application """
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from flask import Flask
from frontui import BASE_DIR
from frontui.views.public import public_ui
from frontui.views.member import member_ui
from frontui.views.customer import customer_ui


def create_app(app_mode='DEBUG'):
    """ Create application, register blueprints, etc """
    if app_mode == '':
        app_mode = os.environ.get('APP_MODE', 'DEBUG')
    # create an application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'\x88~\x17h\xdc;,\x9f\x1do\x98\xcd\xaf|\x1c\x19\xec\xcf\xb1\x12\xd4\x8b\xcdQ'
    # set logging
    configure_logging(app_mode, app)
    if app_mode == 'DEBUG':
        # debugging in VSCode works only if following 2 lines are commented out
        #app.debug = True
        #app.config['DEBUG'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # register blueprints
    app.register_blueprint(public_ui)
    app.register_blueprint(member_ui)
    app.register_blueprint(customer_ui)
    # register jinja exts
    app.add_template_filter(f=points, name='points')
    # configure uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    # app started
    logging.info('Application started in %s mode', app_mode)
    return app


def configure_logging(app_mode, app):
    logHandler = None
    if app_mode == 'DEBUG':
        # create console handler
        logHandler = logging.StreamHandler()
    elif app_mode == 'PROD':
        # create file time rotating handler
        logHandler = TimedRotatingFileHandler(
            filename=os.environ.get('APP_LOG_FILENAME', 'app.log'),
            when='D',
            backupCount=5,
            encoding='UTF-8'
        )
    if logHandler is None:
        return
    logHandler.setLevel(logging.DEBUG)
    logHandler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(name)-10s %(levelname)-7s %(message)s',
        datefmt='%H:%M:%S'))
    # get root logger
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logHandler)
    app.logger.setLevel(logging.DEBUG)
    return


def points(answer, question):
    return str(question.cost) if answer == 'yes' else '0' if answer == 'no' else ''
