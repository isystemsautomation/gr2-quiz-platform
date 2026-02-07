# SEO Fixes - Production Release

## Priority Issues Fixed

### 1. ✅ Hardcoded production domain in templates and structured data
**Issue**: Login/register canonicals and OG tags hardcoded `quiz.isystemsautomation.com`, causing wrong URLs in staging/multi-domain deploys.

**Fix**: 
- Created `quiz/templatetags/site_urls.py` template tag `{% site_url %}`
- All templates now use dynamic URLs from `SITE_DOMAIN` setting
- Updated all JSON-LD structured data in views to use `build_absolute_https_url()`
- Replaced all `request.build_absolute_uri()` calls with `build_absolute_https_url(request, path)`

**Files Changed**:
- `quiz/templates/registration/login.html` - Dynamic URLs
- `quiz/templates/accounts/register.html` - Dynamic URLs
- `quiz/templates/learn/subject_list.html` - Dynamic URLs
- `quiz/templates/learn/subject_detail.html` - Dynamic URLs
- `quiz/templates/learn/block_detail.html` - Dynamic URLs
- `quiz/templates/learn/question_detail.html` - Dynamic URLs
- `quiz/learn_views.py` - All structured data uses `build_absolute_https_url()`

### 2. ✅ Mixed URL-generation strategy
**Issue**: Some views used `build_absolute_https_url()`, others used `request.build_absolute_uri()`, causing inconsistent scheme/host under proxies.

**Fix**: 
- Standardized all absolute URLs to use `build_absolute_https_url(request, path)`
- Removed all `request.build_absolute_uri()` calls
- Ensures consistent HTTPS scheme and fixed domain

**Files Changed**:
- `quiz/learn_views.py` - Replaced all `request.build_absolute_uri()` calls
- `quiz/templates/learn/question_detail.html` - Uses `{% site_url request.path %}`
- `quiz/templates/learn/subject_detail.html` - Uses `{% site_url request.path %}`

### 3. ✅ Duplicate subject source definitions
**Issue**: `list_subjects()` duplicated across `quiz/views.py`, `quiz/learn_views.py`, and `quiz/sitemaps.py`, risking slug/title mismatch.

**Fix**: 
- Created centralized `quiz/subjects.py` module
- Single source of truth for subject metadata
- All modules now import from `quiz.subjects`

**Files Changed**:
- `quiz/subjects.py` - New centralized module
- `quiz/views.py` - Imports from `quiz.subjects`
- `quiz/learn_views.py` - Imports from `quiz.subjects`
- `quiz/sitemaps.py` - Imports from `quiz.subjects`
- `quiz/utils.py` - Imports from `quiz.subjects`

**Note**: `quiz/loader.py` keeps its own `list_subjects()` that loads titles from JSON files (for dynamic title loading). This is intentional and used for data import.

### 4. ✅ Slug parsing fallback is brittle
**Issue**: `parse_subject_slug` fallback logic could fail for hyphenated IDs and cause 404s.

**Fix**: 
- Simplified to exact slug map matching
- Builds complete slug map for all known subjects
- Improved legacy format fallback (checks suffix matching)
- More reliable and maintainable

**Files Changed**:
- `quiz/utils.py` - Improved `parse_subject_slug()` logic

### 5. ✅ Potentially indexable auth pages
**Issue**: Login/register pages used `index, follow`, diluting crawl budget.

**Fix**: 
- Changed to `noindex, follow` on login and register pages
- Preserves link equity while preventing indexing
- Focuses crawl budget on `/learn/` pages

**Files Changed**:
- `quiz/templates/registration/login.html` - `noindex, follow`
- `quiz/templates/accounts/register.html` - `noindex, follow`

## Additional SEO Improvements

### Internal Linking
- Breadcrumbs already provide internal linking structure
- Question pages link to parent blocks
- Block pages link to parent subjects
- Subject pages link to all blocks

### Unique Titles and Descriptions
- All learn pages have unique titles based on subject/block/question
- Meta descriptions are context-specific
- Question pages use truncated question text in descriptions

### Lastmod Consistency
- Sitemaps already include `lastmod` based on `edited_at` timestamps
- Subject sitemaps use latest question edit time
- Block sitemaps use latest question edit time in block
- Question sitemaps use question `edited_at`

## Testing Recommendations

1. **Domain Consistency**: Test with different `SITE_DOMAIN` values - all URLs should update
2. **Canonical URLs**: Verify all pages have correct canonical URLs
3. **Structured Data**: Validate JSON-LD with Google's Rich Results Test
4. **Robots Meta**: Verify login/register are `noindex, follow`
5. **Slug Parsing**: Test old format slugs (e.g., `legislatie-gr-2-legislatie-gr-2`) - should parse correctly

## Production Deployment Notes

- **SITE_DOMAIN** must be set in production environment
- All URLs will use this domain consistently
- Auth pages will not be indexed (preserves crawl budget)
- Subject metadata is centralized (prevents inconsistencies)

