from flask import Flask
from config import config
from app.extensions import db, login_manager, migrate, csrf


def create_app(config_name="default"):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.tasks import tasks_bp
    from app.routes.logs import logs_bp
    from app.routes.envs import envs_bp
    from app.routes.alerts import alerts_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(envs_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(api_bp)

    return app
