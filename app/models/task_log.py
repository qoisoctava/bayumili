from app.extensions import db
from datetime import datetime


class TaskLog(db.Model):
    __tablename__ = "task_logs"

    id = db.Column(db.Integer, primary_key=True)
    task_run_id = db.Column(db.Integer, db.ForeignKey("task_runs.id"), nullable=False)
    level = db.Column(db.Enum("INFO", "WARNING", "ERROR", "DEBUG"), default="INFO")
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TaskLog {self.level} - {self.created_at}>"
