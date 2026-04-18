from app.extensions import db
from datetime import datetime


class AlertConfig(db.Model):
    __tablename__ = "alert_configs"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    trigger = db.Column(
        db.Enum("on_failure", "on_retry_exhausted", "on_sla_breach", "on_success"),
        nullable=False,
    )
    channel = db.Column(db.Enum("email"), default="email")
    recipient = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AlertConfig {self.task_id} - {self.trigger}>"
