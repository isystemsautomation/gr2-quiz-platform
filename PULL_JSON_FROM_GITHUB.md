# Pull JSON Files from GitHub to Server

This guide explains how to update JSON files on the server by pulling changes from GitHub.

## ⚠️ Important Warning

**Pulling JSON files from GitHub will overwrite your auto-synced JSON files from the database!**

If you have custom explanations or changes in your database that aren't in GitHub, they will be lost. The auto-sync will recreate them, but only if the questions still exist in the database.

## Scenario 1: Pull Code Changes (Keep Local JSON Files)

If you want to pull code changes from GitHub but **keep your local auto-synced JSON files**:

```bash
cd /opt/gr2-quiz/gr2-quiz-platform

# Pull changes (JSON files won't be updated because of skip-worktree)
git pull origin main

# Restart the service if needed
sudo systemctl restart gr2quiz
```

The JSON files will remain untouched because `--skip-worktree` is enabled.

## Scenario 2: Pull JSON Files from GitHub (Overwrite Local)

If you want to **replace your local JSON files with the versions from GitHub**:

### Step 1: SSH to Server
```bash
ssh ubuntu@quiz.isystemsautomation.com
```

### Step 2: Go to Project Directory
```bash
cd /opt/gr2-quiz/gr2-quiz-platform
```

### Step 3: Backup Current JSON Files (Optional but Recommended)
```bash
# Create backup directory
mkdir -p ~/json_backup_$(date +%Y%m%d_%H%M%S)

# Copy JSON files
cp quiz_data/*.json ~/json_backup_$(date +%Y%m%d_%H%M%S)/
```

### Step 4: Remove Skip-Worktree
This allows Git to update the JSON files:
```bash
git update-index --no-skip-worktree quiz_data/electrotehnica.json
git update-index --no-skip-worktree quiz_data/legislatie-gr-2.json
git update-index --no-skip-worktree quiz_data/norme-tehnice-gr-2.json
```

### Step 5: Pull from GitHub
```bash
git pull origin main
```

This will update the JSON files from GitHub.

### Step 6: Re-Enable Skip-Worktree (IMPORTANT!)
After pulling, re-enable skip-worktree so auto-sync doesn't conflict:
```bash
git update-index --skip-worktree quiz_data/electrotehnica.json
git update-index --skip-worktree quiz_data/legislatie-gr-2.json
git update-index --skip-worktree quiz_data/norme-tehnice-gr-2.json
```

### Step 7: (Optional) Re-import JSON to Database
If you want to update the database with the JSON files from GitHub:

```bash
# Activate virtual environment
source .venv/bin/activate

# Import questions (this will update the database)
python manage.py import_questions
```

**Note**: This will overwrite any custom explanations in the database with the versions from the JSON files.

### Step 8: Restart Service
```bash
sudo systemctl restart gr2quiz
```

## Quick One-Liner (Pull JSON from GitHub)

```bash
cd /opt/gr2-quiz/gr2-quiz-platform && \
git update-index --no-skip-worktree quiz_data/*.json && \
git pull origin main && \
git update-index --skip-worktree quiz_data/*.json
```

## Check What Will Change (Before Pulling)

To see what differences exist between your local JSON and GitHub:

```bash
# Remove skip-worktree temporarily
git update-index --no-skip-worktree quiz_data/*.json

# Fetch latest from GitHub
git fetch origin main

# Compare your local files with GitHub version
git diff origin/main -- quiz_data/electrotehnica.json
git diff origin/main -- quiz_data/legislatie-gr-2.json
git diff origin/main -- quiz_data/norme-tehnice-gr-2.json

# Re-enable skip-worktree
git update-index --skip-worktree quiz_data/*.json
```

## Troubleshooting

### If Pull Fails with "Your local changes would be overwritten"

This means skip-worktree is still active. Remove it first:
```bash
git update-index --no-skip-worktree quiz_data/*.json
git pull origin main
git update-index --skip-worktree quiz_data/*.json
```

### If You Want to Merge Instead of Overwrite

If there are conflicts between local and GitHub versions:
```bash
# Remove skip-worktree
git update-index --no-skip-worktree quiz_data/*.json

# Pull and merge
git pull origin main

# Resolve any conflicts manually, then:
git add quiz_data/*.json
git commit -m "Merge JSON files from GitHub"

# Re-enable skip-worktree
git update-index --skip-worktree quiz_data/*.json
```

### Check Current Skip-Worktree Status

To see which files have skip-worktree enabled:
```bash
git ls-files -v | grep "^S" | grep json
```

If you see the JSON files listed, skip-worktree is active.

## Recommended Workflow

1. **For regular code updates**: Just `git pull` (JSON files stay untouched)
2. **For JSON updates from GitHub**: Follow Scenario 2 above
3. **For pushing local JSON to GitHub**: Use `UPDATE_JSON_MANUAL.md`


