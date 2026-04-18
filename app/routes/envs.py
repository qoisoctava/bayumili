from flask import Blueprint

envs_bp = Blueprint("envs", __name__, url_prefix="/envs")


@envs_bp.route("/")
def index():
    return "envs - coming soon"
