import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.models.alert_config import AlertConfig


def send_alert(task, run, trigger):
    """
    Send alert email based on trigger type.
    Only sends if there is an active alert config for this task + trigger.
    """
    # Find active alert configs for this task and trigger
    alerts = AlertConfig.query.filter_by(
        task_id=task.id, trigger=trigger, is_active=True
    ).all()

    if not alerts:
        return

    for alert in alerts:
        try:
            send_email(recipient=alert.recipient, task=task, run=run, trigger=trigger)
            print(f"Alert sent to {alert.recipient} for trigger {trigger}")
        except Exception as e:
            print(f"Failed to send alert to {alert.recipient}: {e}")


def build_email_body(task, run, trigger):
    """Build HTML email body"""

    # Trigger labels
    trigger_labels = {
        "on_failure": "❌ Task Failed",
        "on_retry_exhausted": "⚠️ Retries Exhausted",
        "on_sla_breach": "⏰ SLA Breached",
        "on_success": "✅ Task Succeeded",
    }

    label = trigger_labels.get(trigger, trigger)
    duration = f"{run.duration:.1f}s" if run.duration else "-"

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #333;">{label}</h2>
        <hr>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px; font-weight: bold;">Task</td>
                <td style="padding: 8px;">{task.name}</td>
            </tr>
            <tr style="background: #f5f5f5;">
                <td style="padding: 8px; font-weight: bold;">Status</td>
                <td style="padding: 8px;">{run.status.upper()}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold;">Trigger</td>
                <td style="padding: 8px;">{trigger}</td>
            </tr>
            <tr style="background: #f5f5f5;">
                <td style="padding: 8px; font-weight: bold;">Attempt</td>
                <td style="padding: 8px;">{run.attempt}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold;">Duration</td>
                <td style="padding: 8px;">{duration}</td>
            </tr>
            <tr style="background: #f5f5f5;">
                <td style="padding: 8px; font-weight: bold;">Started At</td>
                <td style="padding: 8px;">
                    {run.started_at.strftime('%Y-%m-%d %H:%M:%S') if run.started_at else '-'}
                </td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold;">Finished At</td>
                <td style="padding: 8px;">
                    {run.finished_at.strftime('%Y-%m-%d %H:%M:%S') if run.finished_at else '-'}
                </td>
            </tr>
        </table>
        <hr>
        <p style="color: #888; font-size: 12px;">
            This email was sent automatically by BayuMili Scheduler.
        </p>
    </body>
    </html>
    """
    return html


def send_email(recipient, task, run, trigger):
    """Send email via SMTP"""
    import os

    smtp_host = os.getenv("SMTP_HOST", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)

    # Build subject
    trigger_subjects = {
        "on_failure": f"[BayuMili] ❌ Task Failed: {task.name}",
        "on_retry_exhausted": f"[BayuMili] ⚠️ Retries Exhausted: {task.name}",
        "on_sla_breach": f"[BayuMili] ⏰ SLA Breached: {task.name}",
        "on_success": f"[BayuMili] ✅ Task Succeeded: {task.name}",
    }
    subject = trigger_subjects.get(trigger, f"[BayuMili] Alert: {task.name}")

    # Build email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_from
    msg["To"] = recipient

    html_body = build_email_body(task, run, trigger)
    msg.attach(MIMEText(html_body, "html"))

    # Send
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)
        server.sendmail(smtp_from, recipient, msg.as_string())
