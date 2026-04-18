from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.extensions import db
from app.models.task import Task
from app.models.task_run import TaskRun
from app.forms import TaskForm
from app.utils import admin_required
from croniter import croniter

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_cron(expression):
    """Validate cron expression"""
    try:
        croniter(expression)
        return True
    except Exception:
        return False


# ✅ Public - anyone can view task list
@tasks_bp.route("/")
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("tasks/index.html", tasks=tasks)


# ✅ Public - anyone can view task detail
@tasks_bp.route("/<int:id>")
def detail(id):
    task = Task.query.get_or_404(id)
    runs = (
        TaskRun.query.filter_by(task_id=id)
        .order_by(TaskRun.created_at.desc())
        .limit(10)
        .all()
    )
    return render_template("tasks/detail.html", task=task, runs=runs)


# ❌ Admin only - create task
@tasks_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    form = TaskForm()

    if form.validate_on_submit():
        # Validate cron expression
        if not validate_cron(form.cron_expression.data):
            flash("Invalid cron expression.", "danger")
            return render_template("tasks/form.html", form=form, title="Create Task")

        # Check duplicate name
        existing = Task.query.filter_by(name=form.name.data).first()
        if existing:
            flash("Task name already exists.", "danger")
            return render_template("tasks/form.html", form=form, title="Create Task")

        task = Task(
            name=form.name.data,
            description=form.description.data,
            script_path=form.script_path.data,
            cron_expression=form.cron_expression.data,
            retries=form.retries.data,
            retry_delay=form.retry_delay.data,
            sla_minutes=form.sla_minutes.data,
            is_active=form.is_active.data,
        )

        db.session.add(task)
        db.session.commit()

        flash(f'Task "{task.name}" created successfully!', "success")
        return redirect(url_for("tasks.index"))

    return render_template("tasks/form.html", form=form, title="Create Task")


# ❌ Admin only - edit task
@tasks_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def edit(id):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        # Validate cron expression
        if not validate_cron(form.cron_expression.data):
            flash("Invalid cron expression.", "danger")
            return render_template(
                "tasks/form.html", form=form, title="Edit Task", task=task
            )

        # Check duplicate name (exclude current task)
        existing = Task.query.filter(Task.name == form.name.data, Task.id != id).first()
        if existing:
            flash("Task name already exists.", "danger")
            return render_template(
                "tasks/form.html", form=form, title="Edit Task", task=task
            )

        task.name = form.name.data
        task.description = form.description.data
        task.script_path = form.script_path.data
        task.cron_expression = form.cron_expression.data
        task.retries = form.retries.data
        task.retry_delay = form.retry_delay.data
        task.sla_minutes = form.sla_minutes.data
        task.is_active = form.is_active.data

        db.session.commit()
        flash(f'Task "{task.name}" updated successfully!', "success")
        return redirect(url_for("tasks.detail", id=task.id))

    return render_template("tasks/form.html", form=form, title="Edit Task", task=task)


# ❌ Admin only - delete task
@tasks_bp.route("/<int:id>/delete", methods=["POST"])
@admin_required
def delete(id):
    task = Task.query.get_or_404(id)
    name = task.name
    db.session.delete(task)
    db.session.commit()
    flash(f'Task "{name}" deleted successfully!', "success")
    return redirect(url_for("tasks.index"))


# ❌ Admin only - toggle active status
@tasks_bp.route("/<int:id>/toggle", methods=["POST"])
@admin_required
def toggle(id):
    task = Task.query.get_or_404(id)
    task.is_active = not task.is_active
    db.session.commit()
    status = "activated" if task.is_active else "deactivated"
    flash(f'Task "{task.name}" {status} successfully!', "success")
    return redirect(url_for("tasks.detail", id=task.id))


# ❌ Admin only - manual trigger
@tasks_bp.route("/<int:id>/trigger", methods=["POST"])
@admin_required
def trigger(id):
    task = Task.query.get_or_404(id)

    # Create a new task run
    run = TaskRun(task_id=task.id, status="pending", triggered_by="manual")
    db.session.add(run)
    db.session.commit()

    flash(f'Task "{task.name}" triggered manually! Run ID: {run.id}', "success")
    return redirect(url_for("tasks.detail", id=task.id))
