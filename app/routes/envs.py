from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from app.extensions import db
from app.models.env_var import EnvVar
from app.forms import EnvVarForm
from app.utils import admin_required, encrypt_value, decrypt_value, mask_value

envs_bp = Blueprint("envs", __name__, url_prefix="/envs")


# ❌ Admin only - view env vars list
@envs_bp.route("/")
@admin_required
def index():
    env_vars = EnvVar.query.order_by(EnvVar.key).all()
    return render_template("envs/index.html", env_vars=env_vars)


# ❌ Admin only - create env var
@envs_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    form = EnvVarForm()

    if form.validate_on_submit():
        # Check duplicate key
        existing = EnvVar.query.filter_by(key=form.key.data).first()
        if existing:
            flash(f'Key "{form.key.data}" already exists.', "danger")
            return render_template("envs/form.html", form=form, title="Create Env Var")

        # Encrypt value
        encrypted = encrypt_value(form.value.data)

        env_var = EnvVar(
            key=form.key.data,
            encrypted_value=encrypted,
            description=form.description.data,
        )

        db.session.add(env_var)
        db.session.commit()

        flash(f'Env var "{env_var.key}" created successfully!', "success")
        return redirect(url_for("envs.index"))

    return render_template("envs/form.html", form=form, title="Create Env Var")


# ❌ Admin only - edit env var
@envs_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def edit(id):
    env_var = EnvVar.query.get_or_404(id)
    form = EnvVarForm()

    if form.validate_on_submit():
        # Check duplicate key (exclude current)
        existing = EnvVar.query.filter(
            EnvVar.key == form.key.data, EnvVar.id != id
        ).first()
        if existing:
            flash(f'Key "{form.key.data}" already exists.', "danger")
            return render_template(
                "envs/form.html", form=form, title="Edit Env Var", env_var=env_var
            )

        # Encrypt new value
        encrypted = encrypt_value(form.value.data)

        env_var.key = form.key.data
        env_var.encrypted_value = encrypted
        env_var.description = form.description.data

        db.session.commit()
        flash(f'Env var "{env_var.key}" updated successfully!', "success")
        return redirect(url_for("envs.index"))

    # Pre-fill form with existing data (except value)
    form.key.data = env_var.key
    form.description.data = env_var.description

    return render_template(
        "envs/form.html", form=form, title="Edit Env Var", env_var=env_var
    )


# ❌ Admin only - delete env var
@envs_bp.route("/<int:id>/delete", methods=["POST"])
@admin_required
def delete(id):
    env_var = EnvVar.query.get_or_404(id)
    key = env_var.key
    db.session.delete(env_var)
    db.session.commit()
    flash(f'Env var "{key}" deleted successfully!', "success")
    return redirect(url_for("envs.index"))


# ❌ Admin only - unmask/reveal value
@envs_bp.route("/<int:id>/reveal", methods=["POST"])
@admin_required
def reveal(id):
    env_var = EnvVar.query.get_or_404(id)
    try:
        decrypted = decrypt_value(env_var.encrypted_value)
        return jsonify({"success": True, "value": decrypted})
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to decrypt value."})
