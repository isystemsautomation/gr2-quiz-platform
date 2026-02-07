# Code Review Fixes - Production Release

## Issues Fixed

### 1. ✅ High: Rate-limit bypass via spoofed X-Forwarded-For
**Issue**: Rate limiter trusted `HTTP_X_FORWARDED_FOR` directly, which clients can spoof.

**Fix**: 
- Only trust `X-Forwarded-For` when `DJANGO_USE_X_FORWARDED_PROTO` is enabled (behind proxy)
- Otherwise use `REMOTE_ADDR` which cannot be spoofed
- Prevents brute-force bypass by rotating fake IP headers

**Code**: `quiz/rate_limit.py` lines 28-37

### 2. ✅ High: Background thread DB/file export causes SQLite lock errors
**Issue**: `post_save`/`post_delete` spawned threads that queried/wrote immediately, causing "database table is locked" errors.

**Fix**: 
- Replaced threading with `transaction.on_commit()`
- Export happens after transaction commits, avoiding lock conflicts
- Maintains non-blocking behavior without SQLite issues

**Code**: `quiz/signals.py` - Updated to use `transaction.on_commit()`

### 3. ✅ Medium: N+1 query patterns on dashboard
**Issue**: Per-block queries in loops (attempt lookup) degraded performance.

**Fix**: 
- Single query to fetch all attempts for subject/user
- Group by block_number in Python
- Reduces N queries to 1 query per subject

**Code**: `quiz/views.py` lines 49-65

### 4. ✅ Medium: Hardcoded production domain in templates/JSON-LD
**Issue**: Several pages hardcoded `https://quiz.isystemsautomation.com` in canonical/OG/structured data.

**Fix**: 
- Created `quiz/templatetags/site_urls.py` template tag
- Added `{% site_url %}` tag that uses `SITE_DOMAIN` setting
- Updated all templates to use dynamic URLs
- Updated `learn_views.py` to use `build_absolute_https_url()` helper

**Code**: 
- `quiz/templatetags/site_urls.py` - New template tag
- `quiz/templates/registration/login.html` - Updated URLs
- `quiz/templates/accounts/register.html` - Updated URLs
- `quiz/templates/learn/subject_list.html` - Updated URLs
- `quiz/templates/learn/block_detail.html` - Updated URLs
- `quiz/learn_views.py` - Updated JSON-LD structured data

### 5. ✅ Medium: parse_subject_slug compatibility fallback is logically broken
**Issue**: Fallback split slug by last `-` and compared only final token to subject IDs. IDs like `legislatie-gr-2` could never match ("2" vs full ID).

**Fix**: 
- Updated fallback to check if slug ends with `-{subject_id}` or equals `subject_id`
- Verifies against expected slug format
- Properly handles both old and new slug formats

**Code**: `quiz/utils.py` lines 183-195

### 6. ✅ Low: Middleware documentation vs behavior mismatch
**Issue**: Docstring said logout is exempt, but `/accounts/logout/` was not in exempt_paths.

**Fix**: 
- Updated docstring to clarify that logout is POST-only and enforced by view decorator
- Removed misleading reference to logout exemption in middleware

**Code**: `quiz/middleware.py` lines 10-18

### 7. ✅ Low: Unused imports cleanup
**Issue**: Many unused imports across views, learn_views, etc.

**Fix**: 
- Removed unused imports from `quiz/views.py`:
  - `login`, `authenticate` (not used)
  - `UserCreationForm` (not used)
  - `HttpResponseRedirect` (not used)
  - `csrf_exempt` (not used)
  - `Max`, `Q` from `django.db.models` (not used)

**Code**: `quiz/views.py` lines 1-11

## Files Changed

### New Files
- `quiz/templatetags/__init__.py` - Template tags package
- `quiz/templatetags/site_urls.py` - Site URL template tag
- `CODE_REVIEW_FIXES.md` - This file

### Modified Files
- `quiz/rate_limit.py` - Fixed IP spoofing vulnerability
- `quiz/signals.py` - Fixed SQLite lock errors (transaction.on_commit)
- `quiz/views.py` - Fixed N+1 queries, removed unused imports
- `quiz/utils.py` - Fixed parse_subject_slug fallback logic
- `quiz/middleware.py` - Fixed documentation
- `quiz/templates/registration/login.html` - Dynamic URLs
- `quiz/templates/accounts/register.html` - Dynamic URLs
- `quiz/templates/learn/subject_list.html` - Dynamic URLs
- `quiz/templates/learn/block_detail.html` - Dynamic URLs
- `quiz/learn_views.py` - Dynamic URLs in JSON-LD
- `quiz/middleware.py` - Removed unused imports
- `quiz/sitemaps.py` - Removed unused imports

## Testing Recommendations

1. **Rate Limiting**: Test with spoofed `X-Forwarded-For` header - should use `REMOTE_ADDR` when not behind proxy
2. **SQLite Locks**: Test concurrent question edits - should not produce lock errors
3. **N+1 Queries**: Monitor database queries on dashboard - should be minimal
4. **Dynamic URLs**: Test with different `SITE_DOMAIN` values - URLs should update correctly
5. **Slug Parsing**: Test old format slugs (e.g., `legislatie-gr-2-legislatie-gr-2`) - should parse correctly

## Production Deployment Notes

- **Rate limiting** now properly handles proxy scenarios
- **SQLite** lock issues resolved (consider PostgreSQL for production)
- **Performance** improved with optimized queries
- **URLs** are now dynamic and respect `SITE_DOMAIN` setting
- **Code quality** improved with unused import cleanup

