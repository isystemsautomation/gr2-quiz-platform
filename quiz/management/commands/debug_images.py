"""
Debug command to check if images are being found correctly.
"""
from django.core.management.base import BaseCommand
from quiz.models import Question
from quiz.utils import get_question_image_url, get_option_image_url
from pathlib import Path
from django.conf import settings


class Command(BaseCommand):
    help = 'Debug image detection for questions'

    def add_arguments(self, parser):
        parser.add_argument('--qid', type=int, help='Check specific question ID')
        parser.add_argument('--subject', type=str, help='Check specific subject')

    def handle(self, *args, **options):
        qid = options.get('qid')
        subject = options.get('subject')
        
        if qid and subject:
            questions = Question.objects.filter(qid=qid, subject=subject)
        elif qid:
            questions = Question.objects.filter(qid=qid)
        elif subject:
            questions = Question.objects.filter(subject=subject)[:5]
        else:
            questions = Question.objects.all()[:10]
        
        self.stdout.write(f"Checking {questions.count()} questions...\n")
        
        for question in questions:
            self.stdout.write(f"\nQuestion {question.qid} ({question.subject}, Block {question.block_number}):")
            self.stdout.write(f"  Image base: '{question.image_base or f'q{question.qid}'}'")
            
            # Check question image
            exists, url = get_question_image_url(question, question.subject)
            self.stdout.write(f"  Question image: {'✓' if exists else '✗'} {url or 'NOT FOUND'}")
            
            # Check option images
            for opt_num, opt_letter in [(1, 'A'), (2, 'B'), (3, 'C')]:
                exists, url = get_option_image_url(question, question.subject, opt_num)
                self.stdout.write(f"  Option {opt_letter} image: {'✓' if exists else '✗'} {url or 'NOT FOUND'}")
            
            # Show expected paths
            from quiz.utils import get_image_prefix
            if question.image_base:
                base = question.image_base
            else:
                prefix = get_image_prefix(question.subject)
                base = f"{prefix}{question.qid}"
            expected_path = Path(settings.BASE_DIR) / 'static' / 'img' / question.subject / f"{base}.png"
            self.stdout.write(f"  Expected path: {expected_path}")
            self.stdout.write(f"  Path exists: {expected_path.exists()}")

