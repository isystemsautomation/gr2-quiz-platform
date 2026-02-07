"""
Django signals for automatic JSON synchronization.
Automatically exports questions to JSON files when they are saved.
Uses transaction.on_commit to avoid SQLite lock errors.
"""
import json
from pathlib import Path
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings
from .models import Question


# Thread-local storage to track if we're in a bulk import
# This prevents auto-export during bulk operations
import threading
_skip_auto_export = threading.local()


def set_skip_auto_export(value=True):
    """Set flag to skip auto-export (useful during bulk imports)."""
    _skip_auto_export.value = value


def get_skip_auto_export():
    """Get current skip auto-export flag."""
    return getattr(_skip_auto_export, 'value', False)


def export_subject_to_json(subject_id):
    """
    Export a single subject's questions to JSON file.
    This is the same logic as export_questions command but for one subject.
    """
    try:
        base_dir = Path(settings.BASE_DIR)
        quiz_data_dir = base_dir / 'quiz_data'
        
        mapping = {
            "electrotehnica": "electrotehnica.json",
            "legislatie-gr-2": "legislatie-gr-2.json",
            "norme-tehnice-gr-2": "norme-tehnice-gr-2.json",
        }
        
        if subject_id not in mapping:
            return
        
        filename = mapping[subject_id]
        out_path = quiz_data_dir / filename
        
        # Try to preserve existing top-level metadata (title, blockSize, etc.)
        base_data = {}
        if out_path.exists():
            try:
                base_data = json.loads(out_path.read_text(encoding="utf-8"))
            except Exception:
                base_data = {}
        
        title = base_data.get("title") or subject_id.replace("-", " ").title()
        block_size = base_data.get("blockSize", 20)
        
        # Get all questions for this subject
        questions_qs = (
            Question.objects.filter(subject=subject_id)
            .order_by("qid")
        )
        
        questions = []
        for q in questions_qs:
            questions.append({
                "id": q.qid,
                "question": q.text,
                "options": {
                    "a": q.option_a,
                    "b": q.option_b,
                    "c": q.option_c,
                },
                "correct": q.correct,
                "explanation": q.explanation or "",
                "block": q.block_number,
                "image_base": q.image_base or None,
            })
        
        export_data = {
            "title": title,
            "subject": subject_id,
            "blockSize": block_size,
            "questionCount": len(questions),
            "questions": questions,
        }
        
        # Write to file
        out_path.write_text(
            json.dumps(export_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        # Log error but don't break the save operation
        import logging
        logger = logging.getLogger('quiz.signals')
        logger.error(f"Failed to auto-export {subject_id} to JSON: {e}", exc_info=True)


@receiver(post_save, sender=Question)
def auto_export_question(sender, instance, created, **kwargs):
    """
    Automatically export questions to JSON when saved.
    Skips during bulk imports to avoid performance issues.
    Uses transaction.on_commit to avoid SQLite lock errors.
    """
    # Skip if we're in a bulk import operation
    if get_skip_auto_export():
        return
    
    # Export only the affected subject
    # Use transaction.on_commit to avoid SQLite lock errors
    # This ensures the export happens after the transaction commits
    transaction.on_commit(
        lambda: export_subject_to_json(instance.subject)
    )


@receiver(post_delete, sender=Question)
def auto_export_question_delete(sender, instance, **kwargs):
    """
    Automatically export when a question is deleted.
    Uses transaction.on_commit to avoid SQLite lock errors.
    """
    if get_skip_auto_export():
        return
    
    # Store subject_id before instance is deleted
    subject_id = instance.subject
    
    transaction.on_commit(
        lambda: export_subject_to_json(subject_id)
    )

