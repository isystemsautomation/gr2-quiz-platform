# Manual JSON Update from Server to GitHub

## Simple Steps

### 1. SSH to Server
```bash
ssh ubuntu@quiz.isystemsautomation.com
```

### 2. Go to Project Directory
```bash
cd /opt/gr2-quiz/gr2-quiz-platform
```

### 3. Remove Skip-Worktree (Temporarily)
This allows Git to see your changes:
```bash
git update-index --no-skip-worktree quiz_data/electrotehnica.json
git update-index --no-skip-worktree quiz_data/legislatie-gr-2.json
git update-index --no-skip-worktree quiz_data/norme-tehnice-gr-2.json
```

### 4. Check What Changed
```bash
git status
```

### 5. Add JSON Files
```bash
git add quiz_data/electrotehnica.json
git add quiz_data/legislatie-gr-2.json
git add quiz_data/norme-tehnice-gr-2.json
```

Or all at once:
```bash
git add quiz_data/*.json
```

### 6. Commit
```bash
git commit -m "Update JSON files from database"
```

### 7. Push to GitHub
```bash
git push origin main
```

### 8. Re-Enable Skip-Worktree (IMPORTANT!)
After pushing, re-enable skip-worktree so Git doesn't overwrite your files:
```bash
git update-index --skip-worktree quiz_data/electrotehnica.json
git update-index --skip-worktree quiz_data/legislatie-gr-2.json
git update-index --skip-worktree quiz_data/norme-tehnice-gr-2.json
```

### 9. Verify
```bash
git status
```
The JSON files should NOT show as modified anymore.

## Quick One-Liner (All Steps)

```bash
cd /opt/gr2-quiz/gr2-quiz-platform && \
git update-index --no-skip-worktree quiz_data/*.json && \
git add quiz_data/*.json && \
git commit -m "Update JSON files from database" && \
git push origin main && \
git update-index --skip-worktree quiz_data/*.json
```

## Check Current Status

To see if skip-worktree is active:
```bash
git ls-files -v | grep "^S" | grep json
```

If you see the JSON files listed, skip-worktree is active.

## Troubleshooting

### If Git Says "Nothing to Commit"
The JSON files might not have changed, or skip-worktree is still active. Check:
```bash
git diff quiz_data/electrotehnica.json
```

### If Push Fails (Permission Denied)
Configure Git credentials:
```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

Or use SSH keys for authentication.

### If There Are Conflicts
If GitHub has different versions:
```bash
# Remove skip-worktree
git update-index --no-skip-worktree quiz_data/*.json

# Pull and resolve
git pull origin main

# Resolve conflicts, then:
git add quiz_data/*.json
git commit -m "Resolve conflicts"
git push origin main

# Re-enable skip-worktree
git update-index --skip-worktree quiz_data/*.json
```



