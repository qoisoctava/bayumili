from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    IntegerField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(
                min=3, max=80, message="Username must be between 3 and 80 characters"
            ),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Password is required")]
    )
    submit = SubmitField("Login")


class TaskForm(FlaskForm):
    name = StringField(
        "Task Name",
        validators=[
            DataRequired(message="Task name is required"),
            Length(
                min=3, max=120, message="Task name must be between 3 and 120 characters"
            ),
        ],
    )
    description = TextAreaField("Description", validators=[Optional()])
    script_path = StringField(
        "Script Path",
        validators=[DataRequired(message="Script path is required"), Length(max=255)],
    )
    cron_expression = StringField(
        "Cron Expression",
        validators=[
            DataRequired(message="Cron expression is required"),
            Length(max=100),
        ],
    )
    retries = IntegerField(
        "Retries",
        default=0,
        validators=[
            NumberRange(min=0, max=10, message="Retries must be between 0 and 10")
        ],
    )
    retry_delay = IntegerField(
        "Retry Delay (minutes)",
        default=5,
        validators=[
            NumberRange(
                min=1, max=60, message="Retry delay must be between 1 and 60 minutes"
            )
        ],
    )
    sla_minutes = IntegerField("SLA (minutes)", validators=[Optional()])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Task")
