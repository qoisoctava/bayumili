from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models.alert_config import AlertConfig
from app.models.task import Task
from app.forms import AlertConfigForm
from app.utils import admin_required

alerts_bp = Blueprint("alerts", __name__, url_prefix="/alerts")


# ❌ Admin only - view alert configs
@alerts_bp.route("/")
@admin_required
def index():
    alerts = AlertConfig.query.order_by(AlertConfig.task_id).all()
    return render_template("alerts/index.html", alerts=alerts)


# ❌ Admin only - create alert config
@alerts_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    form = AlertConfigForm()

    # Populate task choices
    tasks = Task.query.order_by(Task.name).all()
    form.task_id.choices = [(t.id, t.name) for t in tasks]

    if not tasks:
        flash("Please create a task first before adding alert config.", "warning")
        return redirect(url_for("alerts.index"))

    if form.validate_on_submit():
        # Check duplicate alert (same task + trigger)
        existing = AlertConfig.query.filter_by(
            task_id=form.task_id.data, trigger=form.trigger.data
        ).first()
        if existing:
            flash("An alert with the same task and trigger already exists.", "danger")
            return render_template("alerts/form.html", form=form, title="Create Alert")

        alert = AlertConfig(
            task_id=form.task_id.data,
            trigger=form.trigger.data,
            channel=form.channel.data,
            recipient=form.recipient.data,
            is_active=form.is_active.data,
        )

        db.session.add(alert)
        db.session.commit()

        flash("Alert config created successfully!", "success")
        return redirect(url_for("alerts.index"))

    return render_template("alerts/form.html", form=form, title="Create Alert")


# ❌ Admin only - edit alert config
@alerts_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def edit(id):
    alert = AlertConfig.query.get_or_404(id)
    form = AlertConfigForm(obj=alert)

    # Populate task choices
    tasks = Task.query.order_by(Task.name).all()
    form.task_id.choices = [(t.id, t.name) for t in tasks]

    if form.validate_on_submit():
        # Check duplicate (exclude current)
        existing = AlertConfig.query.filter(
            AlertConfig.task_id == form.task_id.data,
            AlertConfig.trigger == form.trigger.data,
            AlertConfig.id != id,
        ).first()
        if existing:
            flash("An alert with the same task and trigger already exists.", "danger")
            return render_template(
                "alerts/form.html", form=form, title="Edit Alert", alert=alert
            )

        alert.task_id = form.task_id.data
        alert.trigger = form.trigger.data
        alert.channel = form.channel.data
        alert.recipient = form.recipient.data
        alert.is_active = form.is_active.data

        db.session.commit()
        flash("Alert config updated successfully!", "success")
        return redirect(url_for("alerts.index"))

    return render_template(
        "alerts/form.html", form=form, title="Edit Alert", alert=alert
    )


# ❌ Admin only - delete alert config
@alerts_bp.route("/<int:id>/delete", methods=["POST"])
@admin_required
def delete(id):
    alert = AlertConfig.query.get_or_404(id)
    db.session.delete(alert)
    db.session.commit()
    flash("Alert config deleted successfully!", "success")
    return redirect(url_for("alerts.index"))


# ❌ Admin only - toggle alert active status
@alerts_bp.route("/<int:id>/toggle", methods=["POST"])
@admin_required
def toggle(id):
    alert = AlertConfig.query.get_or_404(id)
    alert.is_active = not alert.is_active
    db.session.commit()
    status = "activated" if alert.is_active else "deactivated"
    flash(f"Alert {status} successfully!", "success")
    return redirect(url_for("alerts.index"))
