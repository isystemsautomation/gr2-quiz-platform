"""
Utility functions for quiz application.
"""
import os
from pathlib import Path
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.utils.text import slugify


def build_absolute_https_url(request, path=''):
    """
    Build an absolute HTTPS URL from a request and path.
    Ensures HTTPS is used even if request is HTTP.
    
    Args:
        request: Django request object
        path: URL path (defaults to request.path if empty)
    
    Returns:
        str: Absolute HTTPS URL
    """
    if not path:
        path = request.path
    
    # Get host from request
    host = request.get_host()
    
    # Ensure HTTPS
    scheme = 'https'
    
    # Build absolute URL
    return f"{scheme}://{host}{path}"


def check_static_file_exists(relative_path):
    """
    Check if a static file exists and return (exists, url).
    
    Args:
        relative_path: Relative path from static root, e.g. 'img/electrotehnica/q123.png'
    
    Returns:
        tuple: (exists: bool, url: str)
    """
    # Normalize path separators
    relative_path = relative_path.replace('\\', '/')
    
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
    
    # Additional fallback: check in BASE_DIR/static/
    base_dir = Path(settings.BASE_DIR)
    static_path = base_dir / 'static' / relative_path
    if static_path.exists():
        url = f"{settings.STATIC_URL}{relative_path}"
        return True, url
    
    return False, None


def get_image_prefix(subject):
    """
    Get the image prefix based on subject.
    qe = electrotehnica
    ql = legislatie-gr-2
    qn = norme-tehnice-gr-2
    """
    prefix_map = {
        'electrotehnica': 'qe',
        'legislatie-gr-2': 'ql',
        'norme-tehnice-gr-2': 'qn',
    }
    return prefix_map.get(subject, 'q')


def get_question_image_url(question, subject):
    """
    Get the URL for a question's main image if it exists.
    
    Returns:
        tuple: (exists: bool, url: str or None)
    """
    if question.image_base:
        # Custom image base provided
        base = question.image_base
    else:
        # Use subject prefix: qe, ql, or qn
        prefix = get_image_prefix(subject)
        base = f"{prefix}{question.qid}"
    
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
    if question.image_base:
        # Custom image base provided
        base = question.image_base
    else:
        # Use subject prefix: qe, ql, or qn
        prefix = get_image_prefix(subject)
        base = f"{prefix}{question.qid}"
    
    relative_path = f"img/{subject}/{base}_{option_number}.png"
    exists, url = check_static_file_exists(relative_path)
    return exists, url if exists else None


def get_subject_slug(subject_id, subject_title):
    """
    Generate a stable, unique slug for a subject.
    Format: slugified-title-id (only append id if different from title_slug)
    Example: 'electrotehnica' -> 'electrotehnica'
             'legislatie-gr-2' -> 'legislatie-gr-2' (no duplicate)
    """
    title_slug = slugify(subject_title)
    # Only append subject_id if it's different from the slugified title
    if title_slug == subject_id:
        return subject_id
    return f"{title_slug}-{subject_id}"


def get_block_slug(subject_id, block_number):
    """
    Generate a stable, unique slug for a block.
    Format: bloc-{number}-{subject_id}
    Example: block 1 in electrotehnica -> 'bloc-1-electrotehnica'
    """
    return f"bloc-{block_number}-{subject_id}"


def parse_subject_slug(slug):
    """
    Parse a subject slug back to subject_id.
    Returns subject_id or None if invalid.
    Handles both formats: "subject-id" and "slugified-title-subject-id"
    """
    # First, try to find exact match with get_subject_slug
    try:
        from .learn_views import list_subjects
    except ImportError:
        from .views import list_subjects
    
    for subj in list_subjects():
        expected_slug = get_subject_slug(subj['id'], subj['title'])
        if expected_slug == slug:
            return subj['id']
    
    # Fallback: check if slug is just the subject_id
    valid_subject_ids = [s['id'] for s in list_subjects()]
    if slug in valid_subject_ids:
        return slug
    
    # Fallback: try to extract from end (for old format compatibility)
    parts = slug.rsplit('-', 1)
    if len(parts) == 2 and parts[1] in valid_subject_ids:
        # Check if this matches any subject's expected slug
        for subj in list_subjects():
            if get_subject_slug(subj['id'], subj['title']) == slug:
                return subj['id']
    
    return None


def parse_block_slug(slug):
    """
    Parse a block slug back to (subject_id, block_number).
    Format: bloc-{number}-{subject_id}
    Returns (subject_id, block_number) or (None, None) if invalid.
    """
    # Block slugs are: bloc-{number}-{subject_id}
    if not slug.startswith('bloc-'):
        return None, None
    
    # Get valid subject IDs first
    try:
        from .learn_views import list_subjects
    except ImportError:
        from .views import list_subjects
    valid_subjects = [s['id'] for s in list_subjects()]
    
    # Remove 'bloc-' prefix
    remaining = slug[5:]
    
    # Try each valid subject_id to find a match
    # We need to find where the block number ends and subject_id begins
    for subject_id in valid_subjects:
        # Check if slug ends with this subject_id
        if remaining.endswith(f'-{subject_id}'):
            # Extract block number (everything before the subject_id)
            block_part = remaining[:-len(f'-{subject_id}')]
            try:
                block_number = int(block_part)
                return subject_id, block_number
            except ValueError:
                continue
    
    return None, None

