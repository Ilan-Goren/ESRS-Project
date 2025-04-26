"""
Security utilities for the restaurant management system.

This module contains functions for enhancing the security of the application,
including password validation, input sanitization, and CSRF protection.
"""

import re
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError


def validate_password_strength(password):
    """
    Validate that a password meets minimum security requirements.
    
    Args:
        password (str): The password to validate.
    
    Raises:
        ValidationError: If the password doesn't meet security requirements.
    """
    if len(password) < 8:
        raise ValidationError(
            "This password is too short. It must contain at least 8 characters."
        )
    
    if not any(char.isdigit() for char in password):
        raise ValidationError(
            "This password must contain at least 1 digit."
        )
    
    if not any(char.isupper() for char in password):
        raise ValidationError(
            "This password must contain at least 1 uppercase letter."
        )
    
    if not any(char.islower() for char in password):
        raise ValidationError(
            "This password must contain at least 1 lowercase letter."
        )
    
    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password):
        raise ValidationError(
            "This password must contain at least 1 special character."
        )


def sanitize_input(input_str):
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        input_str (str): The input string to sanitize.
    
    Returns:
        str: The sanitized input string.
    """
    if not input_str:
        return input_str
    
    # Escape HTML special characters
    sanitized = escape(input_str)
    
    return sanitized


def sanitize_and_allow_basic_tags(input_str):
    """
    Sanitize user input but allow basic HTML tags like <b>, <i>, <br>.
    
    Args:
        input_str (str): The input string to sanitize.
    
    Returns:
        str: The sanitized input string with allowed HTML tags.
    """
    if not input_str:
        return input_str
    
    # Escape HTML special characters
    sanitized = escape(input_str)
    
    # Define allowed tags with their attributes
    allowed_tags = {
        'b': [],
        'strong': [],
        'i': [],
        'em': [],
        'br': [],
        'p': [],
        'ul': [],
        'ol': [],
        'li': [],
    }
    
    # Replace escaped tags with their unescaped versions
    for tag, attrs in allowed_tags.items():
        # Opening tags
        sanitized = re.sub(
            r'&lt;' + tag + r'&gt;',
            '<' + tag + '>',
            sanitized
        )
        
        # Closing tags
        sanitized = re.sub(
            r'&lt;/' + tag + r'&gt;',
            '</' + tag + '>',
            sanitized
        )
    
    return mark_safe(sanitized)


def is_valid_email(email):
    """
    Check if an email address is valid.
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    # Basic email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone):
    """
    Check if a phone number is valid.
    
    Args:
        phone (str): The phone number to validate.
    
    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    # Remove any non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if we have a reasonable number of digits (7-15)
    return 7 <= len(digits_only) <= 15


def format_phone_number(phone):
    """
    Format a phone number for display.
    
    Args:
        phone (str): The phone number to format.
    
    Returns:
        str: The formatted phone number.
    """
    # Remove any non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # If it's a common 10-digit US format
    if len(digits_only) == 10:
        return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    
    # If it's a common 11-digit format with country code
    elif len(digits_only) == 11 and digits_only[0] == '1':
        return f"+1 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"
    
    # Otherwise, just return the original
    return phone