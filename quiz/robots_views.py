"""
Robots.txt view for SEO.
"""
from django.http import HttpResponse
from django.conf import settings


def robots_txt(request):
    """
    Generate robots.txt content.
    Allows crawling of /learn/ pages, disallows admin and private routes.
    """
    domain = getattr(settings, 'SITE_DOMAIN', request.get_host())
    protocol = 'https' if request.is_secure() else 'http'
    sitemap_url = f"{protocol}://{domain}/sitemap.xml"
    
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
    return HttpResponse(content, content_type='text/plain')

