from datetime import datetime, timedelta
from croniter import croniter
from app.extensions import db
from app.models.task import Task
from app.models.task_run import TaskRun
from app.models.task_log import TaskLog


def get_due_tasks():
    """Get all active tasks that are due to run"""
    now = datetime.utcnow()
    due_tasks = []

    tasks = Task.query.filter_by(is_active=True).all()

    for task in tasks:
        try:
            cron = croniter(task.cron_expression, now - timedelta(minutes=1))
            next_run = cron.get_next(datetime)

            # If next run is within the current minute window
            if next_run <= now:
                # Check if already running
                already_running = TaskRun.query.filter_by(
                    task_id=task.id, status="running"
                ).first()

                if not already_running:
                    due_tasks.append(task)
        except Exception as e:
            print(f"Error checking task {task.name}: {e}")

    return due_tasks


def create_task_run(task, triggered_by="scheduler"):
    """Create a new TaskRun record"""
    run = TaskRun(
        task_id=task.id, status="pending", triggered_by=triggered_by, attempt=1
    )
    db.session.add(run)
    db.session.commit()
    return run


def log_message(run_id, level, message):
    """Save a log entry for a task run"""
    log = TaskLog(task_run_id=run_id, level=level, message=message)
    db.session.add(log)
    db.session.commit()


def tick():
    """
    Main heartbeat function.
    Called every minute by the cPanel cron job.
    """
    from app.scheduler.worker import execute_task

    now = datetime.utcnow()
    print(f"[{now}] Scheduler tick started...")

    due_tasks = get_due_tasks()

    if not due_tasks:
        print(f"[{now}] No tasks due.")
        return {"executed": 0}

    executed = 0
    for task in due_tasks:
        try:
            print(f"[{now}] Running task: {task.name}")
            run = create_task_run(task, triggered_by="scheduler")
            execute_task(task, run)
            executed += 1
        except Exception as e:
            print(f"[{now}] Error executing task {task.name}: {e}")

    return {"executed": executed}
