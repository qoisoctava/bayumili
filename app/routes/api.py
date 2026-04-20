from flask import Blueprint, jsonify
from app.extensions import csrf

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health")
def health():
    return jsonify({"status": "ok"})


# Exempt from CSRF - called by cPanel cron job
@csrf.exempt
@api_bp.route("/scheduler/heartbeat", methods=["GET", "POST"])
def heartbeat():
    """
    Called every minute by cPanel cron job [1]:
    */1 * * * * curl -s https://domain.com/api/scheduler/heartbeat
    """
    try:
        from app.scheduler.engine import tick

        result = tick()
        return jsonify({"status": "ok", "executed": result["executed"]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route("/scheduler/run/<int:task_id>", methods=["POST"])
def manual_run(task_id):
    """Manually trigger a task via API"""
    try:
        from app.models.task import Task
        from app.scheduler.engine import create_task_run
        from app.scheduler.worker import execute_task

        task = Task.query.get_or_404(task_id)
        run = create_task_run(task, triggered_by="manual")
        execute_task(task, run)

        return jsonify({"status": "ok", "run_id": run.id, "task": task.name})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
