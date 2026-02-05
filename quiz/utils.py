"""
Utility functions for quiz application.
"""
import os
from pathlib import Path
from django.conf import settings
from django.contrib.staticfiles.finders import find


def check_static_file_exists(relative_path):
    """
    Check if a static file exists and return (exists, url).
    
    Args:
        relative_path: Relative path from static root, e.g. 'img/electrotehnica/q123.png'
    
    Returns:
        tuple: (exists: bool, url: str)
    """
    # Try to find the file using Django's staticfiles finders
    found_path = find(relative_path)
    
    if found_path and os.path.exists(found_path):
        from django.contrib.staticfiles.storage import staticfiles_storage
        url = staticfiles_storage.url(relative_path)
        return True, url
    
    # Fallback: check in STATICFILES_DIRS
    for static_dir in settings.STATICFILES_DIRS:
        full_path = Path(static_dir) / relative_path
        if full_path.exists():
            url = f"{settings.STATIC_URL}{relative_path}"
            return True, url
    
    return False, None


def get_question_image_url(question, subject):
    """
    Get the URL for a question's main image if it exists.
    
    Returns:
        tuple: (exists: bool, url: str or None)
    """
    base = question.image_base if question.image_base else f"q{question.qid}"
    relative_path = f"img/{subject}/{base}.png"
    exists, url = check_static_file_exists(relative_path)
    return exists, url if exists else None


def get_option_image_url(question, subject, option_number):
    """
    Get the URL for an option's image if it exists.
    option_number: 1 for A, 2 for B, 3 for C
    
    Returns:
        tuple: (exists: bool, url: str or None)
    """
    base = question.image_base if question.image_base else f"q{question.qid}"
    relative_path = f"img/{subject}/{base}_{option_number}.png"
    exists, url = check_static_file_exists(relative_path)
    return exists, url if exists else None

