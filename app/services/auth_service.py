"""Authentication service layer"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models.user import User
from app.utils.logger import logger, log_security_event
from app.utils.exceptions import AuthenticationError, ValidationError
from flask import request


class AuthService:
    """Service layer for authentication operations"""
    
    @staticmethod
    def authenticate_user(username: str, password: str, ip_address: str = None) -> User:
        """Authenticate user with username and password"""
        try:
            # Validate input
            if not username or not password:
                raise ValidationError("Username and password are required")
            
            # Find user by username
            user = User.query.filter_by(username=username).first()
            
            if not user:
                log_security_event('login_failed_username', ip_address, request.headers.get('User-Agent'), 
                                 f"Username not found: {username}")
                raise AuthenticationError("Invalid username or password")
            
            # Check password
            if not user.check_password(password):
                log_security_event('login_failed_password', ip_address, request.headers.get('User-Agent'), 
                                 f"Invalid password for user: {username}")
                raise AuthenticationError("Invalid username or password")
            
            # Check if user is active (if you have an active field)
            if hasattr(user, 'is_active') and not user.is_active:
                log_security_event('login_failed_inactive', ip_address, request.headers.get('User-Agent'), 
                                 f"Inactive user attempted login: {username}")
                raise AuthenticationError("Account is disabled")
            
            # Log successful login
            log_security_event('login_success', ip_address, request.headers.get('User-Agent'), 
                             f"User logged in: {username}")
            
            # Update last login time
            if hasattr(user, 'last_login'):
                user.last_login = datetime.utcnow()
                db.session.commit()
            
            return user
            
        except (ValidationError, AuthenticationError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
            raise AuthenticationError("Authentication failed")
    
    @staticmethod
    def login_user(user: User, remember: bool = False) -> bool:
        """Log in user using Flask-Login"""
        try:
            return login_user(user, remember=remember)
        except Exception as e:
            logger.error(f"Error during user login: {str(e)}")
            return False
    
    @staticmethod
    def logout_user() -> None:
        """Log out current user"""
        try:
            username = current_user.username if current_user.is_authenticated else "anonymous"
            logout_user()
            log_security_event('logout_success', request.remote_addr, request.headers.get('User-Agent'), 
                             f"User logged out: {username}")
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
    
    @staticmethod
    def create_user(username: str, email: str, password: str, **kwargs) -> User:
        """Create a new user"""
        try:
            # Validate input
            if not username or len(username.strip()) < 3:
                raise ValidationError("Username must be at least 3 characters long")
            
            if not email or not AuthService._validate_email(email):
                raise ValidationError("Valid email address is required")
            
            if not password or len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long")
            
            # Check if username already exists
            if User.query.filter_by(username=username).first():
                raise ValidationError("Username already exists")
            
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                raise ValidationError("Email address already registered")
            
            # Create user
            user = User(
                username=username.strip(),
                email=email.strip(),
                **kwargs
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"Created new user: {username}")
            return user
            
        except (ValidationError, Exception):
            db.session.rollback()
            raise
    
    @staticmethod
    def update_password(user: User, current_password: str, new_password: str) -> bool:
        """Update user password"""
        try:
            # Validate current password
            if not user.check_password(current_password):
                raise AuthenticationError("Current password is incorrect")
            
            # Validate new password
            if not new_password or len(new_password) < 8:
                raise ValidationError("New password must be at least 8 characters long")
            
            # Update password
            user.set_password(new_password)
            db.session.commit()
            
            logger.info(f"Password updated for user: {user.username}")
            return True
            
        except (ValidationError, AuthenticationError, Exception):
            db.session.rollback()
            raise
    
    @staticmethod
    def get_current_user() -> Optional[User]:
        """Get currently authenticated user"""
        try:
            return current_user if current_user.is_authenticated else None
        except:
            return None
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if current user is authenticated"""
        try:
            return current_user.is_authenticated
        except:
            return False
    
    @staticmethod
    def require_authentication() -> User:
        """Get current user or raise authentication error"""
        user = AuthService.get_current_user()
        if not user:
            raise AuthenticationError("Authentication required")
        return user
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def get_login_stats(days: int = 30) -> Dict[str, Any]:
        """Get login statistics for monitoring"""
        try:
            since_date = datetime.utcnow() - timedelta(days=days)
            
            # This would require a login_logs table in a real implementation
            # For now, return mock data
            return {
                'total_logins': 150,
                'successful_logins': 145,
                'failed_logins': 5,
                'unique_users': 3,
                'recent_logins': [
                    {
                        'username': 'admin',
                        'timestamp': datetime.utcnow().isoformat(),
                        'ip_address': '127.0.0.1'
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error getting login stats: {str(e)}")
            return {
                'total_logins': 0,
                'successful_logins': 0,
                'failed_logins': 0,
                'unique_users': 0,
                'recent_logins': []
            }
