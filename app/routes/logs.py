from flask import Blueprint

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")


@logs_bp.route("/")
def index():
    return "logs - coming soon"
