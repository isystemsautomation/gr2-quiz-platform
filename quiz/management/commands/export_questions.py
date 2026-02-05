"""
Export questions from the database back into the JSON files in ``quiz_data/``.

This is the inverse of ``import_questions`` and lets you regenerate clean,
up‑to‑date JSON that includes any corrections you have made in the admin
interface or via the UI (correct answers, explanations, image_base, etc.).

Usage:

    python manage.py export_questions

The command will overwrite:
    quiz_data/electrotehnica.json
    quiz_data/legislatie-gr-2.json
    quiz_data/norme-tehnice-gr-2.json
"""

from pathlib import Path
import json

from django.core.management.base import BaseCommand

from quiz.models import Question


class Command(BaseCommand):
    help = "Export questions from the database back into quiz_data/*.json"

    def handle(self, *args, **options):
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        quiz_data_dir = project_root / "quiz_data"

        mapping = {
            "electrotehnica": "electrotehnica.json",
            "legislatie-gr-2": "legislatie-gr-2.json",
            "norme-tehnice-gr-2": "norme-tehnice-gr-2.json",
        }

        for subject_id, filename in mapping.items():
            out_path = quiz_data_dir / filename
            self.stdout.write(f"Exporting subject '{subject_id}' -> {out_path}")

            # Try to preserve existing top‑level metadata (title, blockSize, etc.)
            base_data = {}
            if out_path.exists():
                try:
                    base_data = json.loads(out_path.read_text(encoding="utf-8"))
                except Exception:
                    base_data = {}

            title = base_data.get("title") or subject_id.replace("-", " ").title()
            block_size = base_data.get("blockSize", 20)

            questions_qs = (
                Question.objects.filter(subject=subject_id)
                .order_by("qid")
            )

            questions = []
            for q in questions_qs:
                questions.append(
                    {
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
                        # keep an ``image`` field only if you are using it;
                        # otherwise you can ignore it in the JSON.
                        # we expose image_base so you can derive filenames if needed
                        "image_base": q.image_base or None,
                    }
                )

            export_data = {
                "title": title,
                "subject": subject_id,
                "blockSize": block_size,
                "questionCount": len(questions),
                "questions": questions,
            }

            out_path.write_text(
                json.dumps(export_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"  -> wrote {len(questions)} questions to {out_path}"
                )
            )


