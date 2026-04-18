from app.extensions import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    script_path = db.Column(db.String(255), nullable=False)
    cron_expression = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    retries = db.Column(db.Integer, default=0)
    retry_delay = db.Column(db.Integer, default=5)  # in minutes
    sla_minutes = db.Column(db.Integer, nullable=True)  # SLA duration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    runs = db.relationship(
        "TaskRun", backref="task", lazy=True, cascade="all, delete-orphan"
    )
    alert_configs = db.relationship(
        "AlertConfig", backref="task", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Task {self.name}>"
