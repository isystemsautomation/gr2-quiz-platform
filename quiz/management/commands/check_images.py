"""
Simple command to check what images exist and what the system expects.
"""
from django.core.management.base import BaseCommand
from pathlib import Path
from django.conf import settings
from quiz.models import Question


class Command(BaseCommand):
    help = 'Check what image files exist vs what the system expects'

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        static_dir = base_dir / 'static' / 'img'
        
        self.stdout.write(f"Checking images in: {static_dir}\n")
        
        if not static_dir.exists():
            self.stdout.write(self.style.ERROR(f"Directory does not exist: {static_dir}"))
            self.stdout.write("Creating directory structure...")
            static_dir.mkdir(parents=True, exist_ok=True)
            (static_dir / 'electrotehnica').mkdir(exist_ok=True)
            (static_dir / 'legislatie-gr-2').mkdir(exist_ok=True)
            (static_dir / 'norme-tehnice-gr-2').mkdir(exist_ok=True)
            self.stdout.write(self.style.SUCCESS("Directories created!"))
            return
        
        subjects = {
            'electrotehnica': 'qe',
            'legislatie-gr-2': 'ql',
            'norme-tehnice-gr-2': 'qn',
        }
        
        for subject, prefix in subjects.items():
            subject_dir = static_dir / subject
            self.stdout.write(f"\n{'='*60}")
            self.stdout.write(f"Subject: {subject} (prefix: {prefix})")
            self.stdout.write(f"Directory: {subject_dir}")
            self.stdout.write(f"{'='*60}")
            
            if not subject_dir.exists():
                self.stdout.write(self.style.WARNING(f"  Directory does not exist!"))
                continue
            
            # List all PNG files
            png_files = list(subject_dir.glob("*.png"))
            
            if not png_files:
                self.stdout.write(self.style.WARNING(f"  No PNG files found!"))
            else:
                self.stdout.write(f"\n  Found {len(png_files)} PNG files:")
                
                # Show first 20 files
                for png_file in sorted(png_files)[:20]:
                    name = png_file.name
                    # Check if it matches expected format
                    if name.startswith(prefix):
                        self.stdout.write(self.style.SUCCESS(f"    ✓ {name}"))
                    elif name.startswith('q'):
                        self.stdout.write(self.style.WARNING(f"    ⚠️  {name} (old format, should start with '{prefix}')"))
                    else:
                        self.stdout.write(f"    ? {name} (unexpected format)")
                
                if len(png_files) > 20:
                    self.stdout.write(f"    ... and {len(png_files) - 20} more files")
        
        # Now check a few questions from database
        self.stdout.write(f"\n\n{'='*60}")
        self.stdout.write("Checking questions from database:")
        self.stdout.write(f"{'='*60}")
        
        for subject, prefix in subjects.items():
            questions = Question.objects.filter(subject=subject)[:5]
            if questions.exists():
                self.stdout.write(f"\n{subject} (expecting prefix '{prefix}'):")
                for q in questions:
                    expected_name = f"{prefix}{q.qid}.png"
                    expected_path = static_dir / subject / expected_name
                    exists = expected_path.exists()
                    status = "✓" if exists else "✗"
                    self.stdout.write(f"  {status} Q{q.qid}: expects {expected_name} -> {exists}")

