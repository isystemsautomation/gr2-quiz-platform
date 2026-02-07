# Production Deployment Guide

## Quick Start

### 1. Server Setup

```bash
# Navigate to project directory
cd /opt/gr2-quiz/gr2-quiz-platform

# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Set these in your systemd service file or `/etc/environment`:

```bash
export DJANGO_DEBUG=false
export DJANGO_SECRET_KEY='your-strong-secret-key-here'
export DJANGO_ALLOWED_HOSTS='quiz.isystemsautomation.com'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://quiz.isystemsautomation.com'
export DJANGO_USE_X_FORWARDED_PROTO=true
export DJANGO_SECURE_SSL_REDIRECT=true
export DJANGO_SECURE_HSTS_SECONDS=31536000
export DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true
export DJANGO_SECURE_HSTS_PRELOAD=true
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create Site record for sitemaps
python manage.py shell
# Then:
from django.contrib.sites.models import Site
site, _ = Site.objects.get_or_create(pk=1)
site.domain = 'quiz.isystemsautomation.com'
site.name = 'Chestionare ANRE Electrician Grupa II'
site.save()
exit()

# Import questions
python manage.py import_questions

# Create superuser
python manage.py createsuperuser
```

### 4. Git Configuration

```bash
# Prevent Git from overwriting auto-synced JSON files
git update-index --skip-worktree quiz_data/electrotehnica.json
git update-index --skip-worktree quiz_data/legislatie-gr-2.json
git update-index --skip-worktree quiz_data/norme-tehnice-gr-2.json
```

### 5. Systemd Service

Ensure `/etc/systemd/system/gr2quiz.service` has:

```ini
[Unit]
Description=GR2 Quiz Django app
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/opt/gr2-quiz/gr2-quiz-platform
Environment="PATH=/opt/gr2-quiz/gr2-quiz-platform/.venv/bin"
Environment="DJANGO_ALLOWED_HOSTS=quiz.isystemsautomation.com,localhost,127.0.0.1"
Environment="DJANGO_CSRF_TRUSTED_ORIGINS=https://quiz.isystemsautomation.com"
ExecStart=/opt/gr2-quiz/gr2-quiz-platform/.venv/bin/python -m gunicorn \
  --workers 3 \
  --bind 127.0.0.1:8000 \
  gr2quiz.wsgi:application

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 6. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl restart gr2quiz.service
sudo systemctl enable gr2quiz.service
sudo systemctl status gr2quiz.service
```

## Verification

1. **Check service**: `sudo systemctl status gr2quiz.service`
2. **Check logs**: `sudo journalctl -u gr2quiz.service -n 50`
3. **Test website**: `https://quiz.isystemsautomation.com/`
4. **Test admin**: `https://quiz.isystemsautomation.com/admin/`
5. **Test auto-export**: Edit a question and check JSON file updates

## Maintenance

### Daily
- Check service status
- Review error logs: `tail -f logs/django.log`

### Weekly
- Backup database: `cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)`
- Review application logs

### Monthly
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Review security updates

## Troubleshooting

### Service won't start
- Check logs: `sudo journalctl -u gr2quiz.service -n 100`
- Verify Python path: `ls -la .venv/bin/python`
- Check permissions: `ls -la db.sqlite3`

### Can't login
- Verify superuser exists: `python manage.py shell` → `User.objects.filter(is_superuser=True)`
- Create new superuser: `python manage.py createsuperuser`

### JSON files not updating
- Check logs: `tail -f logs/django.log`
- Verify signals are loaded: Check `quiz/apps.py`
- Test manually: `python manage.py export_questions`

### 503 Service Unavailable
- Check if service is running: `sudo systemctl status gr2quiz.service`
- Check if gunicorn is running: `ps aux | grep gunicorn`
- Check Apache/Nginx proxy configuration

## Backup and Restore

### Backup
```bash
# Database
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# JSON files (auto-synced, but backup before major changes)
python manage.py export_questions
cp quiz_data/*.json quiz_data/backup/
```

### Restore
```bash
# Stop service
sudo systemctl stop gr2quiz.service

# Restore database
cp db.sqlite3.backup.YYYYMMDD_HHMMSS db.sqlite3

# Fix permissions
sudo chown ubuntu:www-data db.sqlite3

# Restart service
sudo systemctl start gr2quiz.service
```

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS enabled
- [ ] HSTS enabled
- [ ] CSRF protection enabled
- [ ] Secure cookies enabled
- [ ] Admin panel protected
- [ ] Regular backups scheduled

## Support

For issues or questions:
- Check logs: `logs/django.log`
- Check service logs: `sudo journalctl -u gr2quiz.service`
- Review `PRODUCTION_CHECKLIST.md` for detailed checklist

