# Running Django Management Commands on Server

When running Django management commands directly in your shell (not through systemd), you need to set the environment variables manually.

## Quick Solution: Export Environment Variables

### Step 1: Get Secret Key from Systemd Service

```bash
# View the systemd service file to get the secret key
sudo cat /etc/systemd/system/gr2quiz.service | grep DJANGO_SECRET_KEY
```

### Step 2: Export Environment Variables

```bash
# Export all required environment variables
export DJANGO_SECRET_KEY='your-secret-key-from-systemd-service'
export DJANGO_ALLOWED_HOSTS='quiz.isystemsautomation.com,localhost,127.0.0.1'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://quiz.isystemsautomation.com'
export DJANGO_SITE_DOMAIN='quiz.isystemsautomation.com'
export DJANGO_USE_X_FORWARDED_PROTO='true'
export DJANGO_SECURE_SSL_REDIRECT='false'
export DJANGO_DEBUG='false'
```

### Step 3: Run Your Command

```bash
cd /opt/gr2-quiz/gr2-quiz-platform
source .venv/bin/activate
python manage.py import_questions
```

## Alternative: Use systemd-run (Recommended)

This runs the command with the same environment as the service:

```bash
cd /opt/gr2-quiz/gr2-quiz-platform
source .venv/bin/activate

# Run command with systemd service environment
sudo systemd-run --service-type=oneshot \
  --uid=ubuntu \
  --gid=www-data \
  --working-directory=/opt/gr2-quiz/gr2-quiz-platform \
  --setenv=PATH=/opt/gr2-quiz/gr2-quiz-platform/.venv/bin \
  --setenv=DJANGO_SECRET_KEY='your-secret-key' \
  --setenv=DJANGO_ALLOWED_HOSTS='quiz.isystemsautomation.com,localhost,127.0.0.1' \
  --setenv=DJANGO_CSRF_TRUSTED_ORIGINS='https://quiz.isystemsautomation.com' \
  --setenv=DJANGO_SITE_DOMAIN='quiz.isystemsautomation.com' \
  /opt/gr2-quiz/gr2-quiz-platform/.venv/bin/python manage.py import_questions
```

## Create a Helper Script

Create `/opt/gr2-quiz/gr2-quiz-platform/run_command.sh`:

```bash
#!/bin/bash
# Source environment from systemd service
export DJANGO_SECRET_KEY='your-secret-key-here'
export DJANGO_ALLOWED_HOSTS='quiz.isystemsautomation.com,localhost,127.0.0.1'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://quiz.isystemsautomation.com'
export DJANGO_SITE_DOMAIN='quiz.isystemsautomation.com'
export DJANGO_USE_X_FORWARDED_PROTO='true'
export DJANGO_SECURE_SSL_REDIRECT='false'
export DJANGO_DEBUG='false'

cd /opt/gr2-quiz/gr2-quiz-platform
source .venv/bin/activate
exec "$@"
```

Make it executable:
```bash
chmod +x /opt/gr2-quiz/gr2-quiz-platform/run_command.sh
```

Then use it:
```bash
./run_command.sh python manage.py import_questions
./run_command.sh python manage.py createsuperuser
./run_command.sh python manage.py migrate
```

## Common Commands

### Import Questions
```bash
export DJANGO_SECRET_KEY='...'  # (and other vars)
python manage.py import_questions
```

### Create Superuser
```bash
export DJANGO_SECRET_KEY='...'  # (and other vars)
python manage.py createsuperuser
```

### Run Migrations
```bash
export DJANGO_SECRET_KEY='...'  # (and other vars)
python manage.py migrate
```

### Export Questions
```bash
export DJANGO_SECRET_KEY='...'  # (and other vars)
python manage.py export_questions
```

### Django Shell
```bash
export DJANGO_SECRET_KEY='...'  # (and other vars)
python manage.py shell
```

## Security Note

⚠️ **Never commit the secret key to Git!** Always get it from the systemd service file or a secure environment variable store.

