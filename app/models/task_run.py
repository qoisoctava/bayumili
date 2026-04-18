from app.extensions import db
from datetime import datetime


class TaskRun(db.Model):
    __tablename__ = "task_runs"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    status = db.Column(
        db.Enum("pending", "running", "success", "failed", "retrying"),
        default="pending",
    )
    attempt = db.Column(db.Integer, default=1)
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    triggered_by = db.Column(db.Enum("scheduler", "manual"), default="scheduler")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    logs = db.relationship(
        "TaskLog", backref="run", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def duration(self):
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None

    def __repr__(self):
        return f"<TaskRun {self.task_id} - {self.status}>"
