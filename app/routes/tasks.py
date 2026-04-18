from flask import Blueprint

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/")
def index():
    return "tasks - coming soon"
