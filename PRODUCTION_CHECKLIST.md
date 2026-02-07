# Production Release Checklist

## Pre-Deployment Checklist

### 1. Environment Variables
- [ ] Set `DJANGO_DEBUG=false` (CRITICAL: defaults to False, but verify)
- [ ] Set `DJANGO_SECRET_KEY` to a strong random secret (REQUIRED: app will fail without it)
- [ ] Set `DJANGO_ALLOWED_HOSTS` to your domain(s)
- [ ] Set `DJANGO_CSRF_TRUSTED_ORIGINS` to your HTTPS domain(s)
- [ ] Set `DJANGO_SITE_DOMAIN` to your domain (prevents host header poisoning)
- [ ] Set `DJANGO_USE_X_FORWARDED_PROTO=true` (if behind reverse proxy)
- [ ] Set `DJANGO_SECURE_SSL_REDIRECT=true` (after verifying HTTPS works)
- [ ] Set `DJANGO_SECURE_HSTS_SECONDS=31536000` (1 year)
- [ ] Set `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true`
- [ ] Set `DJANGO_SECURE_HSTS_PRELOAD=true`

### 2. Database
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create/update Site record for sitemaps
- [ ] Import questions: `python manage.py import_questions`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Backup database: `cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)`

### 3. Static Files
- [ ] Collect static files: `python manage.py collectstatic` (if using STATIC_ROOT)
- [ ] Verify static files are served correctly
- [ ] Check that CSS and images load properly

### 4. Git Configuration
- [ ] Set skip-worktree for JSON files:
  ```bash
  git update-index --skip-worktree quiz_data/*.json
  ```
- [ ] Verify: `git status` should not show JSON files as modified

### 5. Server Configuration
- [ ] Verify systemd service file is correct
- [ ] Check service status: `sudo systemctl status gr2quiz.service`
- [ ] Verify gunicorn is running: `ps aux | grep gunicorn`
- [ ] Check logs: `sudo journalctl -u gr2quiz.service -n 50`

### 6. Security
- [ ] Verify HTTPS is working
- [ ] Test CSRF protection
- [ ] Verify authentication middleware is working
- [ ] Check that admin panel requires authentication
- [ ] Verify public routes (`/learn/`, `/accounts/login/`) are accessible
- [ ] Test rate limiting: Try 5 failed logins, should get 429 error
- [ ] Verify SECRET_KEY is set (app should fail to start without it in production)
- [ ] Test answer validation: Try submitting invalid answer value, should be rejected

### 7. Functionality Tests
- [ ] Test user registration
- [ ] Test user login
- [ ] Test quiz taking (authenticated)
- [ ] Test public learn mode (unauthenticated)
- [ ] Test question editing (normal user - missing data only)
- [ ] Test question editing (superuser - full access)
- [ ] Test auto-export: Edit a question and verify JSON updates
- [ ] Test sitemap: `/sitemap.xml`
- [ ] Test robots.txt: `/robots.txt`
- [ ] Test license page: `/LICENSE`

### 8. Performance
- [ ] Verify auto-export doesn't block requests (runs in background)
- [ ] Check database query performance
- [ ] Verify static files are cached properly

### 9. Monitoring
- [ ] Set up log rotation for `logs/django.log`
- [ ] Monitor error logs regularly
- [ ] Set up alerts for critical errors

### 10. Documentation
- [ ] Update README.md with production deployment steps
- [ ] Document all environment variables
- [ ] Document backup procedures
- [ ] Document restore procedures

## Post-Deployment Verification

1. **Accessibility**
   - [ ] Homepage loads: `https://quiz.isystemsautomation.com/`
   - [ ] Login page loads: `https://quiz.isystemsautomation.com/accounts/login/`
   - [ ] Public learn mode: `https://quiz.isystemsautomation.com/learn/`
   - [ ] Admin panel: `https://quiz.isystemsautomation.com/admin/`

2. **SEO**
   - [ ] Sitemap accessible: `https://quiz.isystemsautomation.com/sitemap.xml`
   - [ ] Robots.txt accessible: `https://quiz.isystemsautomation.com/robots.txt`
   - [ ] Meta tags are present
   - [ ] Structured data (JSON-LD) is present

3. **Security Headers**
   - [ ] Check HTTPS redirect works
   - [ ] Verify security headers (HSTS, X-Frame-Options, etc.)
   - [ ] Test CSRF protection

4. **Auto-Sync**
   - [ ] Edit a question in admin
   - [ ] Verify JSON file updates automatically
   - [ ] Check logs for any errors

## Rollback Plan

If issues occur:

1. **Stop service**: `sudo systemctl stop gr2quiz.service`
2. **Restore database**: `cp db.sqlite3.backup.YYYYMMDD db.sqlite3`
3. **Restore code**: `git checkout <previous-commit>`
4. **Restart service**: `sudo systemctl start gr2quiz.service`

## Backup Schedule

- **Database**: Daily backups recommended
- **JSON files**: Auto-synced from database, but backup before major changes
- **Code**: Git repository serves as backup

## Maintenance

- **Weekly**: Check logs for errors
- **Monthly**: Review and update dependencies
- **Quarterly**: Review security settings and update if needed

