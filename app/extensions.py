from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

# Login manager settings
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "warning"
