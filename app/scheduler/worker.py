import subprocess
import os
from datetime import datetime
from app.extensions import db
from app.models.task_run import TaskRun
from app.models.task_log import TaskLog
from app.scheduler.engine import log_message


def get_task_env(task):
    """
    Build environment variables for task execution.
    Injects system env + decrypted env vars from database.
    """
    from app.models.env_var import EnvVar
    from app.utils import decrypt_value

    # Start with current system environment
    env = os.environ.copy()

    # Inject all env vars from database
    try:
        env_vars = EnvVar.query.all()
        for ev in env_vars:
            try:
                decrypted = decrypt_value(ev.encrypted_value)
                env[ev.key] = decrypted
            except Exception as e:
                print(f"Failed to decrypt env var {ev.key}: {e}")
    except Exception as e:
        print(f"Failed to load env vars: {e}")

    return env


def execute_task(task, run):
    """
    Execute a task script and update the run status.
    Handles retries, SLA breach, and alerting.
    """
    from app.scheduler.alerting import send_alert

    # Mark as running
    run.status = "running"
    run.started_at = datetime.utcnow()
    db.session.commit()

    log_message(run.id, "INFO", f'Task "{task.name}" started (attempt {run.attempt})')

    success = False
    attempt = run.attempt
    max_attempts = task.retries + 1  # 1 original + N retries

    while attempt <= max_attempts:
        try:
            # Update attempt number
            run.attempt = attempt
            db.session.commit()

            if attempt > 1:
                run.status = "retrying"
                db.session.commit()
                log_message(
                    run.id, "WARNING", f"Retrying attempt {attempt}/{max_attempts}..."
                )

            # Build environment
            env = get_task_env(task)

            # Execute the script
            log_message(run.id, "INFO", f"Executing script: {task.script_path}")

            result = subprocess.run(
                ["python3", task.script_path],
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                env=env,
            )

            # Save stdout
            if result.stdout:
                for line in result.stdout.strip().split("\n"):
                    log_message(run.id, "INFO", line)

            # Save stderr
            if result.stderr:
                for line in result.stderr.strip().split("\n"):
                    log_message(run.id, "WARNING", line)

            if result.returncode == 0:
                success = True
                break
            else:
                log_message(
                    run.id,
                    "ERROR",
                    f"Script exited with return code {result.returncode}",
                )
                # Send on_failure alert
                send_alert(task, run, "on_failure")
                attempt += 1

                # Wait before retry
                if attempt <= max_attempts:
                    import time

                    log_message(
                        run.id,
                        "INFO",
                        f"Waiting {task.retry_delay} minutes before retry...",
                    )
                    time.sleep(task.retry_delay * 60)

        except subprocess.TimeoutExpired:
            log_message(run.id, "ERROR", "Task execution timed out!")
            send_alert(task, run, "on_failure")
            attempt += 1

        except FileNotFoundError:
            log_message(run.id, "ERROR", f"Script not found: {task.script_path}")
            send_alert(task, run, "on_failure")
            break

        except Exception as e:
            log_message(run.id, "ERROR", f"Unexpected error: {str(e)}")
            send_alert(task, run, "on_failure")
            attempt += 1

    # Finished
    run.finished_at = datetime.utcnow()

    if success:
        run.status = "success"
        log_message(run.id, "INFO", f'Task "{task.name}" completed successfully!')
        send_alert(task, run, "on_success")
    else:
        run.status = "failed"
        log_message(
            run.id,
            "ERROR",
            f'Task "{task.name}" failed after {run.attempt} attempt(s)!',
        )
        send_alert(task, run, "on_retry_exhausted")

    # Check SLA breach
    if task.sla_minutes and run.started_at:
        duration_minutes = (run.finished_at - run.started_at).total_seconds() / 60
        if duration_minutes > task.sla_minutes:
            log_message(
                run.id,
                "WARNING",
                f"SLA breached! Took {duration_minutes:.1f} min, SLA is {task.sla_minutes} min",
            )
            send_alert(task, run, "on_sla_breach")

    db.session.commit()
