from flask import Blueprint, render_template
from app.models.task import Task
from app.models.task_run import TaskRun
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")


@dashboard_bp.route("/")
def index():
    # ── Basic Stats ──────────────────────────────
    total_tasks = Task.query.count()
    active_tasks = Task.query.filter_by(is_active=True).count()
    total_runs = TaskRun.query.count()
    success_runs = TaskRun.query.filter_by(status="success").count()
    failed_runs = TaskRun.query.filter_by(status="failed").count()
    running_now = TaskRun.query.filter_by(status="running").count()

    # ── Last 7 Days Stats ────────────────────────
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_runs = TaskRun.query.filter(TaskRun.created_at >= seven_days_ago).count()
    recent_failed = TaskRun.query.filter(
        TaskRun.created_at >= seven_days_ago, TaskRun.status == "failed"
    ).count()

    # ── Recent Task Runs (last 10) ───────────────
    latest_runs = TaskRun.query.order_by(TaskRun.created_at.desc()).limit(10).all()

    # ── Recent Failed Runs ───────────────────────
    failed_recent = (
        TaskRun.query.filter_by(status="failed")
        .order_by(TaskRun.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        total_tasks=total_tasks,
        active_tasks=active_tasks,
        total_runs=total_runs,
        success_runs=success_runs,
        failed_runs=failed_runs,
        running_now=running_now,
        recent_runs=recent_runs,
        recent_failed=recent_failed,
        latest_runs=latest_runs,
        failed_recent=failed_recent,
        datetime=datetime,
    )
