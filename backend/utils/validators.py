"""
Utility validators for input validation
"""

import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """Validate password strength"""
    # At least 6 characters
    if len(password) < 6:
        return False
    return True


def validate_phone(phone: str) -> bool:
    """Validate phone number"""
    # Basic validation: 10 digits
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone.replace('-', '').replace(' ', '')))


def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?:\/\/.+'
    return bool(re.match(pattern, url))


def validate_positive_number(value) -> bool:
    """Validate positive number"""
    try:
        num = float(value)
        return num > 0
    except (ValueError, TypeError):
        return False


def validate_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
    """Validate date format"""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def sanitize_input(input_str: str, max_length: int = 500) -> str:
    """Sanitize user input"""
    if not isinstance(input_str, str):
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = input_str.strip()
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/', 'javascript:']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized
