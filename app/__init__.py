from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import get_config
from .extensions import db, login_manager, migrate
from . import models
from app.models.user import User
from .routes.auth_routes import auth
from .utils.logger import setup_logger, log_error
from .utils.exceptions import PortfolioException
import os
from flask import render_template


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address
    )
    
    # Setup logging
    setup_logger(app)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        log_error(error, "Internal server error")
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(PortfolioException)
    def handle_portfolio_exception(error):
        log_error(error, f"Portfolio exception: {error.message}")
        return {'error': error.message}, error.status_code
    
    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        if app.config.get('ENV') == 'production':
            headers = app.config.get('SECURITY_HEADERS', {})
            for header, value in headers.items():
                response.headers[header] = value
        return response
    
    # Request logging middleware
    @app.before_request
    def log_request_info():
        from flask import request
        app.logger.info(f"Request: {request.method} {request.url} - IP: {request.remote_addr}")
    
    # Register blueprints
    from .routes.main_routes import main
    app.register_blueprint(main)
    
    from .routes.testimonials_stats_routes import testimonials_stats_bp
    app.register_blueprint(testimonials_stats_bp)
    
    from .routes.calendar_routes import calendar_bp
    app.register_blueprint(calendar_bp)
    
    from .routes.about_me_routes import about_me_bp
    app.register_blueprint(about_me_bp)
    
    app.register_blueprint(auth)
    
    from .routes.admin_routes import admin
    app.register_blueprint(admin)
            
    # Create upload directory
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    return app