from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")


@dashboard_bp.route("/")
def index():
    return "dashboard - coming soon"
