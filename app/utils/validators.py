"""Validation utilities for the portfolio application"""

import re
from typing import Any, List


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_required_fields(data: dict, required_fields: List[str]) -> List[str]:
    """Validate that all required fields are present and non-empty"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            missing_fields.append(field)
    
    return missing_fields


def validate_name(name: str) -> bool:
    """Validate name field (letters, spaces, hyphens, apostrophes)"""
    if not name or not isinstance(name, str):
        return False
    
    name = name.strip()
    if len(name) < 2 or len(name) > 100:
        return False
    
    pattern = r'^[a-zA-Z\s\-\'\.]+$'
    return re.match(pattern, name) is not None


def validate_url(url: str) -> bool:
    """Validate URL format"""
    if not url or not isinstance(url, str):
        return True  # Optional field
    
    url = url.strip()
    if not url:
        return True
    
    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    return re.match(pattern, url) is not None


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format"""
    if not phone or not isinstance(phone, str):
        return True  # Optional field
    
    phone = phone.strip()
    if not phone:
        return True
    
    # Remove common formatting characters
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's all digits and reasonable length
    return clean_phone.isdigit() and 10 <= len(clean_phone) <= 15


def validate_text_length(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Validate text length constraints"""
    if not text or not isinstance(text, str):
        return min_length == 0
    
    text = text.strip()
    return min_length <= len(text) <= max_length


def validate_percentage(value: Any) -> bool:
    """Validate percentage value (0-100)"""
    try:
        percentage = float(value)
        return 0 <= percentage <= 100
    except (ValueError, TypeError):
        return False


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for security"""
    if not filename:
        return ""
    
    # Remove path separators and dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    
    # Limit length and remove leading/trailing dots/spaces
    filename = filename.strip('. ').strip()
    
    # Ensure filename is not empty after sanitization
    if not filename:
        filename = "upload"
    
    return filename


def validate_image_file(filename: str) -> bool:
    """Validate image file extension"""
    if not filename:
        return False
    
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)


def validate_project_data(data: dict) -> tuple[bool, List[str]]:
    """Validate project data comprehensively"""
    errors = []
    
    # Required fields
    required_fields = ['title', 'description']
    missing = validate_required_fields(data, required_fields)
    if missing:
        errors.extend([f"Missing required field: {field}" for field in missing])
    
    # Validate title
    if 'title' in data:
        if not validate_text_length(data['title'], 2, 200):
            errors.append("Title must be between 2 and 200 characters")
    
    # Validate description
    if 'description' in data:
        if not validate_text_length(data['description'], 10, 5000):
            errors.append("Description must be between 10 and 5000 characters")
    
    # Validate URLs
    url_fields = ['github_link', 'live_link']
    for field in url_fields:
        if field in data and data[field]:
            if not validate_url(data[field]):
                errors.append(f"Invalid {field.replace('_', ' ')} URL")
    
    return len(errors) == 0, errors


def validate_message_data(data: dict) -> tuple[bool, List[str]]:
    """Validate message data comprehensively"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'email', 'message']
    missing = validate_required_fields(data, required_fields)
    if missing:
        errors.extend([f"Missing required field: {field}" for field in missing])
    
    # Validate name
    if 'name' in data:
        if not validate_name(data['name']):
            errors.append("Invalid name format")
    
    # Validate email
    if 'email' in data:
        if not validate_email(data['email']):
            errors.append("Invalid email address")
    
    # Validate message
    if 'message' in data:
        if not validate_text_length(data['message'], 10, 2000):
            errors.append("Message must be between 10 and 2000 characters")
    
    # Validate subject (optional)
    if 'subject' in data and data['subject']:
        if not validate_text_length(data['subject'], 1, 200):
            errors.append("Subject must be between 1 and 200 characters")
    
    return len(errors) == 0, errors


def validate_skill_data(data: dict) -> tuple[bool, List[str]]:
    """Validate skill data comprehensively"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'percentage']
    missing = validate_required_fields(data, required_fields)
    if missing:
        errors.extend([f"Missing required field: {field}" for field in missing])
    
    # Validate name
    if 'name' in data:
        if not validate_text_length(data['name'], 2, 100):
            errors.append("Skill name must be between 2 and 100 characters")
    
    # Validate percentage
    if 'percentage' in data:
        if not validate_percentage(data['percentage']):
            errors.append("Percentage must be between 0 and 100")
    
    # Validate category (optional)
    if 'category' in data and data['category']:
        if not validate_text_length(data['category'], 2, 50):
            errors.append("Category must be between 2 and 50 characters")
    
    # Validate description (optional)
    if 'description' in data and data['description']:
        if not validate_text_length(data['description'], 1, 500):
            errors.append("Description must be between 1 and 500 characters")
    
    return len(errors) == 0, errors
