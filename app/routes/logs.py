from flask import Blueprint, render_template, request
from app.models.task_log import TaskLog
from app.models.task_run import TaskRun
from app.models.task import Task

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")


# ✅ Public - anyone can view logs
@logs_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    task_id = request.args.get("task_id", None, type=int)
    level = request.args.get("level", None)
    status = request.args.get("status", None)

    # Base query
    query = TaskRun.query

    # Filter by task
    if task_id:
        query = query.filter_by(task_id=task_id)

    # Filter by status
    if status:
        query = query.filter_by(status=status)

    # Paginate
    runs = query.order_by(TaskRun.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # Get all tasks for filter dropdown
    tasks = Task.query.order_by(Task.name).all()

    return render_template(
        "logs/index.html",
        runs=runs,
        tasks=tasks,
        selected_task=task_id,
        selected_level=level,
        selected_status=status,
    )


# ✅ Public - anyone can view run detail logs
@logs_bp.route("/run/<int:run_id>")
def run_detail(run_id):
    run = TaskRun.query.get_or_404(run_id)
    level = request.args.get("level", None)

    # Get logs for this run
    query = TaskLog.query.filter_by(task_run_id=run_id)

    # Filter by level
    if level:
        query = query.filter_by(level=level)

    logs = query.order_by(TaskLog.created_at.asc()).all()

    return render_template(
        "logs/run_detail.html", run=run, logs=logs, selected_level=level
    )
