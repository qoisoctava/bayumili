from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from datetime import datetime, timedelta


def admin_required(f):
    """Only admin (authenticated user) can access this route"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to login to perform this action.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def cleanup_old_logs():
    """Delete logs older than 3 months"""
    from app.extensions import db
    from app.models.task_run import TaskRun
    from app.models.task_log import TaskLog

    cutoff_date = datetime.utcnow() - timedelta(days=90)

    # Find old runs
    old_runs = TaskRun.query.filter(TaskRun.created_at < cutoff_date).all()

    count = 0
    for run in old_runs:
        db.session.delete(run)
        count += 1

    db.session.commit()
    return count
