from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    IntegerField,
    BooleanField,
    SelectField,
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Email


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=80),
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
            Length(min=3, max=120),
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
        "Retries", default=0, validators=[NumberRange(min=0, max=10)]
    )
    retry_delay = IntegerField(
        "Retry Delay (minutes)", default=5, validators=[NumberRange(min=1, max=60)]
    )
    sla_minutes = IntegerField("SLA (minutes)", validators=[Optional()])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Task")


class EnvVarForm(FlaskForm):
    key = StringField(
        "Key",
        validators=[DataRequired(message="Key is required"), Length(min=1, max=120)],
    )
    value = StringField("Value", validators=[DataRequired(message="Value is required")])
    description = StringField("Description", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Save")


class AlertConfigForm(FlaskForm):
    task_id = SelectField(
        "Task", coerce=int, validators=[DataRequired(message="Task is required")]
    )
    trigger = SelectField(
        "Trigger",
        choices=[
            ("on_failure", "On Failure"),
            ("on_retry_exhausted", "On Retry Exhausted"),
            ("on_sla_breach", "On SLA Breach"),
            ("on_success", "On Success"),
        ],
        validators=[DataRequired()],
    )
    channel = SelectField(
        "Channel", choices=[("email", "Email")], validators=[DataRequired()]
    )
    recipient = StringField(
        "Recipient Email",
        validators=[
            DataRequired(message="Recipient email is required"),
            Email(message="Invalid email address"),
            Length(max=120),
        ],
    )
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Alert")
