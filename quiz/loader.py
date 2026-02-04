"""
Quiz data loader utility.
Loads JSON files and provides cached access to quiz questions.
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional

# Cache for loaded quiz data
_quiz_cache = {}


def _get_quiz_data_path():
    """Get the path to quiz_data directory."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / 'quiz_data'


def _load_subject(subject_id: str) -> Dict:
    """Load a subject's JSON file and cache it."""
    if subject_id in _quiz_cache:
        return _quiz_cache[subject_id]
    
    quiz_data_dir = _get_quiz_data_path()
    
    # Map subject IDs to file names
    file_map = {
        'electrotehnica': 'electrotehnica.json',
        'legislatie-gr-2': 'legislatie-gr-2.json',
        'norme-tehnice-gr-2': 'norme-tehnice-gr-2.json',
    }
    
    filename = file_map.get(subject_id)
    if not filename:
        raise ValueError(f"Unknown subject: {subject_id}")
    
    filepath = quiz_data_dir / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Quiz data file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Assign blocks sequentially if not present (20 questions per block)
    questions = data.get('questions', [])
    if questions:
        # Check if any question has a block field
        has_blocks = any('block' in q and q.get('block') is not None for q in questions)
        
        if not has_blocks:
            # Assign blocks: first 20 -> block 1, next 20 -> block 2, etc.
            for i, question in enumerate(questions):
                question['block'] = (i // 20) + 1
    
    _quiz_cache[subject_id] = data
    return data


def list_subjects() -> List[Dict[str, str]]:
    """
    Returns list of subject IDs and titles.
    Returns: [{'id': 'electrotehnica', 'title': '...'}, ...]
    """
    subjects = [
        {'id': 'electrotehnica', 'title': 'Electrotehnică'},
        {'id': 'legislatie-gr-2', 'title': 'Legislație GR. 2'},
        {'id': 'norme-tehnice-gr-2', 'title': 'Norme Tehnice GR. 2'},
    ]
    
    # Load titles from JSON files
    for subject in subjects:
        try:
            data = _load_subject(subject['id'])
            subject['title'] = data.get('title', subject['title'])
        except Exception:
            pass  # Use default title if loading fails
    
    return subjects


def get_blocks(subject: str) -> List[int]:
    """
    Returns sorted list of block numbers present in the subject.
    """
    data = _load_subject(subject)
    questions = data.get('questions', [])
    
    if not questions:
        return []
    
    blocks = set()
    for question in questions:
        block = question.get('block')
        if block is not None:
            blocks.add(block)
    
    return sorted(blocks)


def get_block_questions(subject: str, block_number: int) -> List[Dict]:
    """
    Returns list of question dicts for a specific block.
    """
    data = _load_subject(subject)
    questions = data.get('questions', [])
    
    block_questions = [
        q for q in questions 
        if q.get('block') == block_number
    ]
    
    return block_questions

