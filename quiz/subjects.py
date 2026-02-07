"""
Centralized subject metadata.
Single source of truth for subject IDs, titles, and slugs.
Prevents duplication and ensures consistency across the application.
"""
from typing import List, Dict


def list_subjects() -> List[Dict[str, str]]:
    """
    Returns list of subject IDs and titles.
    This is the single source of truth for subject metadata.
    
    Returns:
        List of dicts with 'id' and 'title' keys
    """
    return [
        {'id': 'electrotehnica', 'title': 'Electrotehnică'},
        {'id': 'legislatie-gr-2', 'title': 'Legislație GR. 2'},
        {'id': 'norme-tehnice-gr-2', 'title': 'Norme Tehnice GR. 2'},
    ]


def get_subject_by_id(subject_id: str) -> Dict[str, str] | None:
    """
    Get subject metadata by ID.
    
    Args:
        subject_id: Subject identifier
        
    Returns:
        Subject dict with 'id' and 'title', or None if not found
    """
    for subject in list_subjects():
        if subject['id'] == subject_id:
            return subject
    return None

