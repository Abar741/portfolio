"""Logging configuration for the portfolio application"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from flask import current_app


def setup_logger(app):
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    if not app.debug and not app.testing:
        log_dir = os.path.join(os.path.dirname(app.instance_path), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure file handler
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'portfolio.log'),
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Portfolio application startup')


# Create a module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add console handler if no handlers exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def log_user_action(action: str, user_id: int = None, details: str = None):
    """Log user actions for audit trail"""
    log_data = {
        'action': action,
        'user_id': user_id,
        'details': details,
        'timestamp': datetime.utcnow().isoformat()
    }
    logger.info(f"User Action: {log_data}")


def log_security_event(event: str, ip_address: str = None, user_agent: str = None, details: str = None):
    """Log security-related events"""
    log_data = {
        'event': event,
        'ip_address': ip_address,
        'user_agent': user_agent,
        'details': details,
        'timestamp': datetime.utcnow().isoformat()
    }
    logger.warning(f"Security Event: {log_data}")


def log_error(error: Exception, context: str = None):
    """Log errors with context"""
    log_data = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context,
        'timestamp': datetime.utcnow().isoformat()
    }
    logger.error(f"Error: {log_data}", exc_info=True)
