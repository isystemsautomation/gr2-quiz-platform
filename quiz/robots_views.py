"""
Robots.txt and LICENSE views for SEO and legal pages.
"""
from django.http import HttpResponse
from django.conf import settings
from pathlib import Path


def robots_txt(request):
    """
    Generate robots.txt content.
    Allows crawling of /learn/ pages, disallows admin and private routes.
    Uses fixed SITE_DOMAIN to prevent host header poisoning.
    """
    # Use fixed domain from settings (prevents host header poisoning)
    domain = getattr(settings, 'SITE_DOMAIN', None)
    if not domain:
        # Fallback only for development
        domain = request.get_host()
    sitemap_url = f"https://{domain}/sitemap.xml"
    
    content = f"""User-agent: *
Allow: /learn/
Allow: /static/
Disallow: /admin/
Disallow: /accounts/
Disallow: /login/
Disallow: /register/
Disallow: /dashboard/
Disallow: /subject/
Disallow: /question/

Sitemap: {sitemap_url}
"""
    return HttpResponse(content, content_type='text/plain; charset=utf-8')


def license_view(request):
    """
    Serve LICENSE file from project root.
    """
    base_dir = Path(settings.BASE_DIR)
    license_path = base_dir / 'LICENSE'
    
    if license_path.exists():
        with open(license_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain; charset=utf-8')
    else:
        return HttpResponse('License file not found.', status=404, content_type='text/plain; charset=utf-8')

