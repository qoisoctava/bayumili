from flask import Blueprint

alerts_bp = Blueprint("alerts", __name__, url_prefix="/alerts")


@alerts_bp.route("/")
def index():
    return "alerts - coming soon"
