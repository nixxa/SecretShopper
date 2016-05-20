"""
The flask application package.
"""
import logging
from flask import Flask
app = Flask(__name__)
app.debug_log_format = '%(asctime)s %(levelname)s %(message)s'
app.logger.setLevel(logging.DEBUG)

import frontui.views
