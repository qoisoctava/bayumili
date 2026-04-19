from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os


def admin_required(f):
    """Only admin (authenticated user) can access this route"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to login to perform this action.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def get_fernet():
    """Get Fernet instance from FERNET_KEY in .env"""
    key = os.getenv("FERNET_KEY")
    if not key:
        raise ValueError("FERNET_KEY is not set in .env")
    return Fernet(key.encode())


def encrypt_value(value: str) -> str:
    """Encrypt a string value using Fernet"""
    f = get_fernet()
    return f.encrypt(value.encode()).decode()


def decrypt_value(encrypted_value: str) -> str:
    """Decrypt a Fernet encrypted string"""
    f = get_fernet()
    return f.decrypt(encrypted_value.encode()).decode()


def mask_value(value: str) -> str:
    """Mask value, show only last 4 characters"""
    if len(value) <= 4:
        return "*" * len(value)
    return "*" * (len(value) - 4) + value[-4:]


def cleanup_old_logs():
    """Delete logs older than 3 months"""
    from app.extensions import db
    from app.models.task_run import TaskRun

    cutoff_date = datetime.utcnow() - timedelta(days=90)

    old_runs = TaskRun.query.filter(TaskRun.created_at < cutoff_date).all()

    count = 0
    for run in old_runs:
        db.session.delete(run)
        count += 1

    db.session.commit()
    return count
