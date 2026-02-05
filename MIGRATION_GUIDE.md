# Migration Guide: JSON to Database Questions

This guide explains the changes made to move from JSON-based questions to database-backed questions with editing capabilities.

## Summary of Changes

### 1. New Database Model: `Question`
- Stores all question data in SQLite
- Fields: subject, qid, block_number, text, option_a/b/c, correct, explanation, image_base, edited_by, edited_at
- Unique constraint on (subject, qid)

### 2. Management Command: `import_questions`
- Imports questions from JSON files into database
- Preserves existing edits (doesn't overwrite correct/explanation/image_base if already set)
- Usage: `python manage.py import_questions`

### 3. Image Handling
- Automatic image detection based on filename patterns
- Images expected in: `static/img/<subject>/`
- Patterns:
  - `q<ID>.png` → question image
  - `q<ID>_1.png` → option A image
  - `q<ID>_2.png` → option B image
  - `q<ID>_3.png` → option C image
- Custom image base can be set via admin or edit form

### 4. User Editing
- **Normal users**: Can fill missing correct answers and explanations
- **Superusers**: Can edit everything via Django Admin or edit form
- Edit link appears on quiz pages for questions missing data

### 5. Updated Views
- Dashboard now uses database to get block counts
- Quiz pages load questions from database
- Grading handles `correct=NULL` gracefully (excludes from total)

## Deployment Steps

1. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Import questions from JSON:**
   ```bash
   python manage.py import_questions
   ```

3. **Restart your server:**
   ```bash
   # If using gunicorn/systemd
   sudo systemctl restart your-service-name
   # Or restart gunicorn manually
   ```

4. **Verify:**
   - Check `/admin/` - Question model should be visible
   - Check dashboard - blocks should load from database
   - Try editing a question with missing data

## File Structure

```
quiz/
├── models.py              # Added Question model
├── admin.py               # Added QuestionAdmin
├── views.py               # Updated to use database
├── utils.py               # NEW: Image handling utilities
├── management/
│   └── commands/
│       └── import_questions.py  # NEW: Import command
├── migrations/
│   └── 0002_question.py   # NEW: Question model migration
└── templates/
    ├── quiz/
    │   ├── block_take.html    # Updated: Shows images, edit links
    │   └── question_edit.html # NEW: Edit form for users
    └── ...

static/
└── img/                   # NEW: Place images here
    ├── electrotehnica/
    ├── legislatie-gr-2/
    └── norme-tehnice-gr-2/
```

## Important Notes

- **JSON files are now seed data only** - they're not used for quiz display
- **User edits are preserved** - import command won't overwrite existing edits
- **Images are optional** - quiz works without images
- **Grading excludes ungradable questions** - questions with `correct=NULL` don't count toward score

## Admin Access

Superusers can edit questions at `/admin/quiz/question/`:
- Edit correct answer
- Edit explanation
- Set custom image base name
- View edit history (edited_by, edited_at)

