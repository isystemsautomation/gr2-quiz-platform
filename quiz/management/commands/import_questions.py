"""
Management command to import questions from JSON files into the database.
Only updates fields that are currently empty/null to preserve user edits.
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils import timezone
from quiz.models import Question


class Command(BaseCommand):
    help = 'Import questions from JSON files in quiz_data/ directory'

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        quiz_data_dir = base_dir / 'quiz_data'
        
        # Map subject IDs to file names
        file_map = {
            'electrotehnica': 'electrotehnica.json',
            'legislatie-gr-2': 'legislatie-gr-2.json',
            'norme-tehnice-gr-2': 'norme-tehnice-gr-2.json',
        }
        
        total_imported = 0
        total_updated = 0
        
        for subject_id, filename in file_map.items():
            filepath = quiz_data_dir / filename
            if not filepath.exists():
                self.stdout.write(self.style.WARNING(f'File not found: {filepath}'))
                continue
            
            self.stdout.write(f'Processing {filename}...')
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions = data.get('questions', [])
            if not questions:
                continue
            
            # Assign blocks if not present (20 questions per block)
            has_blocks = any('block' in q and q.get('block') is not None for q in questions)
            if not has_blocks:
                for i, question in enumerate(questions):
                    question['block'] = (i // 20) + 1
            
            for q_data in questions:
                qid = q_data.get('id')
                if not qid:
                    continue
                
                block_number = q_data.get('block', 1)
                text = q_data.get('question', '')
                options = q_data.get('options', {})
                
                # Get or create question
                question, created = Question.objects.get_or_create(
                    subject=subject_id,
                    qid=qid,
                    defaults={
                        'block_number': block_number,
                        'text': text,
                        'option_a': options.get('a', ''),
                        'option_b': options.get('b', ''),
                        'option_c': options.get('c', ''),
                    }
                )
                
                # Update fields that are currently empty/null (preserve edits)
                updated = False
                if created:
                    total_imported += 1
                    # Set initial values from JSON if provided
                    if q_data.get('correct') is not None:
                        question.correct = q_data.get('correct')
                        updated = True
                    if q_data.get('explanation'):
                        question.explanation = q_data.get('explanation', '')
                        updated = True
                else:
                    # Only update if currently empty/null
                    if not question.correct and q_data.get('correct') is not None:
                        question.correct = q_data.get('correct')
                        updated = True
                    if not question.explanation and q_data.get('explanation'):
                        question.explanation = q_data.get('explanation', '')
                        updated = True
                    # Always update text/options/block_number from JSON (these are the source)
                    if question.text != text:
                        question.text = text
                        updated = True
                    if question.option_a != options.get('a', ''):
                        question.option_a = options.get('a', '')
                        updated = True
                    if question.option_b != options.get('b', ''):
                        question.option_b = options.get('b', '')
                        updated = True
                    if question.option_c != options.get('c', ''):
                        question.option_c = options.get('c', '')
                        updated = True
                    if question.block_number != block_number:
                        question.block_number = block_number
                        updated = True
                
                if updated:
                    question.save()
                    if not created:
                        total_updated += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Import complete: {total_imported} new questions, {total_updated} updated'
        ))

