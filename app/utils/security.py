"""Security utilities for the portfolio application"""

import secrets
import hashlib
from typing import Optional


def generate_csrf_token() -> str:
    """Generate a secure CSRF token"""
    return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    """Hash password using SHA-256 (for demo - use bcrypt in production)"""
    # Note: In production, use bcrypt or argon2 instead of SHA-256
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        salt, stored_hash = hashed_password.split(':')
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash == stored_hash
    except (ValueError, AttributeError):
        return False


def generate_session_token() -> str:
    """Generate a secure session token"""
    return secrets.token_urlsafe(64)


def sanitize_input(input_string: str) -> str:
    """Basic input sanitization"""
    if not input_string:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', 'javascript:', 'vbscript:', 'data:']
    sanitized = input_string
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def is_safe_url(url: str) -> bool:
    """Check if URL is safe for redirect"""
    if not url:
        return False
    
    # Only allow relative URLs or specific safe domains
    safe_domains = ['localhost', '127.0.0.1']
    
    if url.startswith('/') and not url.startswith('//'):
        return True
    
    for domain in safe_domains:
        if domain in url:
            return True
    
    return False
