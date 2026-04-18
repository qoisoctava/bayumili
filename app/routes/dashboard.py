from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")


# No @admin_required here, guests can view dashboard
@dashboard_bp.route("/")
def index():
    return render_template("dashboard/index.html")
