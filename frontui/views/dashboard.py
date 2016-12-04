"""
Dashboard and issue tracker
"""
import logging
from flask import Blueprint, render_template


dashboard_ui = Blueprint("dashboard", __name__)
logger = logging.getLogger(__name__)

@dashboard_ui.route("/dashboard")
def index():
    """
    Render dashboard start page
    """
    return render_template(
        "dashboard.html",
        title='Канбан | Тайный покупатель')
