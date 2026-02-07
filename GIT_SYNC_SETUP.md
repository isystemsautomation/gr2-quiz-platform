# Git Sync Setup - Prevent JSON Overwrite

Since the JSON files in `quiz_data/` are now automatically synced from the database, you need to tell Git to ignore local changes to these files. This prevents Git from overwriting your database-generated JSON files when you pull from GitHub.

## Setup Instructions

### On the Server (After Deployment)

Run these commands to tell Git to ignore local changes to the JSON files:

```bash
cd /opt/gr2-quiz/gr2-quiz-platform

# Tell Git to skip worktree for JSON files (ignore local changes)
git update-index --skip-worktree quiz_data/electrotehnica.json
git update-index --skip-worktree quiz_data/legislatie-gr-2.json
git update-index --skip-worktree quiz_data/norme-tehnice-gr-2.json

# Verify it's working
git status
# The JSON files should not show as modified even if they have local changes
```

### What This Does

- **`--skip-worktree`**: Tells Git to ignore local changes to these files
- The files remain in Git (for seed data)
- But Git won't overwrite them when you pull
- Your auto-synced JSON files from the database will be preserved

### If You Need to Update JSON Files in Git

If you want to commit updated JSON files to Git (e.g., after running `export_questions`):

```bash
# Temporarily remove skip-worktree
git update-index --no-skip-worktree quiz_data/electrotehnica.json
git update-index --no-skip-worktree quiz_data/legislatie-gr-2.json
git update-index --no-skip-worktree quiz_data/norme-tehnice-gr-2.json

# Now you can add and commit
git add quiz_data/*.json
git commit -m "Update JSON files from database"

# Re-enable skip-worktree
git update-index --skip-worktree quiz_data/electrotehnica.json
git update-index --skip-worktree quiz_data/legislatie-gr-2.json
git update-index --skip-worktree quiz_data/norme-tehnice-gr-2.json
```

### Check Current Status

To see which files have skip-worktree enabled:

```bash
git ls-files -v | grep ^S
```

Files with `S` prefix have skip-worktree enabled.

## Alternative: Add to .gitignore (Not Recommended)

If you want to completely ignore JSON files (not track them at all):

1. Add to `.gitignore`:
   ```
   quiz_data/*.json
   ```

2. Remove from Git tracking:
   ```bash
   git rm --cached quiz_data/*.json
   git commit -m "Stop tracking JSON files (auto-generated from database)"
   ```

**Note**: This approach means JSON files won't be in Git at all, so new deployments won't have seed data. The `--skip-worktree` approach is better because it keeps seed data in Git while ignoring local changes.

