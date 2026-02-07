# Security Fixes - Production Release

## Issues Fixed

### 1. ✅ Critical: SECRET_KEY Fallback
**Issue**: Production fallback SECRET_KEY was unsafe - app would use known key if env var missing.

**Fix**: 
- Fail fast in production if `DJANGO_SECRET_KEY` is not set
- Only allow fallback in DEBUG mode (local development)
- Added clear error message with instructions

**Code**: `gr2quiz/settings.py` lines 22-40

### 2. ✅ High: DEBUG Defaults to True
**Issue**: DEBUG defaulted to True, risky if env var missing.

**Fix**: 
- Changed default to `False` for production safety
- Must explicitly set `DJANGO_DEBUG=true` for local development
- Production will fail if SECRET_KEY missing (prevents accidental debug mode)

**Code**: `gr2quiz/settings.py` line 25

### 3. ✅ High: Transport Hardening
**Issue**: Security headers defaulted to disabled.

**Fix**: 
- Security headers now default based on DEBUG mode
- `SECURE_SSL_REDIRECT`, `HSTS`, etc. enabled when `DEBUG=False`
- Documented in `DEPLOYMENT.md` with explicit env var instructions

**Code**: `gr2quiz/settings.py` lines 143-149

### 4. ✅ High: Brute-Force Protection
**Issue**: No rate limiting on login/register endpoints.

**Fix**: 
- Added `quiz/rate_limit.py` decorator
- Login: 5 attempts per 5 minutes per IP
- Registration: 3 attempts per 10 minutes per IP
- Counter resets on successful authentication
- Returns HTTP 429 (Too Many Requests) when limit exceeded

**Code**: 
- `quiz/rate_limit.py` - Rate limiting decorator
- `quiz/auth_views.py` - Applied to login_view and register_view

### 5. ✅ Medium: Host Header Poisoning
**Issue**: Absolute URLs used `request.get_host()` which could be poisoned.

**Fix**: 
- Added `SITE_DOMAIN` setting (from `DJANGO_SITE_DOMAIN` env var)
- Updated `build_absolute_https_url()` to use fixed domain
- Updated `robots_txt()` to use fixed domain
- Fallback to `request.get_host()` only in development if not set

**Code**: 
- `gr2quiz/settings.py` - Added SITE_DOMAIN setting
- `quiz/utils.py` - Updated build_absolute_https_url()
- `quiz/robots_views.py` - Updated robots_txt()

### 6. ✅ Medium: Answer Validation
**Issue**: `correct` answer value not validated server-side.

**Fix**: 
- Added explicit validation: must be 'a', 'b', 'c', or empty
- Returns error message if invalid value provided
- Prevents injection of invalid data

**Code**: `quiz/views.py` lines 260-268

### 7. ✅ Low/Medium: Middleware Cleanup
**Issue**: Inconsistent logic and unused `public_paths` variable.

**Fix**: 
- Removed unused `public_paths` variable
- Consolidated path checking logic
- Updated comments to reflect actual behavior
- Removed dead code

**Code**: `quiz/middleware.py` - Simplified and cleaned up

## New Environment Variables

Add to your production environment:

```bash
export DJANGO_SITE_DOMAIN='quiz.isystemsautomation.com'
```

This prevents host header poisoning in absolute URL generation.

## Testing

### Rate Limiting
1. Try logging in with wrong password 5 times
2. Should see "Prea multe încercări" message
3. Wait 5 minutes or use different IP
4. Should work again

### SECRET_KEY Validation
1. Remove `DJANGO_SECRET_KEY` env var
2. Set `DJANGO_DEBUG=false`
3. App should fail to start with clear error message

### Answer Validation
1. Try to submit invalid answer value (e.g., 'd' or 'x')
2. Should see error message
3. Only 'a', 'b', 'c' should be accepted

## Deployment Notes

- **Rate limiting** uses Django's cache (default: in-memory)
- For production with multiple workers, use Redis or Memcached for shared rate limit state
- **SITE_DOMAIN** must be set in production to prevent host header attacks
- All security fixes are backward compatible (fallbacks for development)

## Additional Recommendations

1. **Use Redis for rate limiting** in multi-worker deployments
2. **Monitor rate limit hits** in logs for security alerts
3. **Set up fail2ban** for additional IP-based blocking
4. **Regular security audits** of authentication endpoints

