"""
Template tags for building absolute URLs using SITE_DOMAIN.
Prevents hardcoded domains in templates.
"""
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def site_url(path=''):
    """
    Build an absolute HTTPS URL using SITE_DOMAIN setting.
    
    Usage:
        {% site_url '/accounts/login/' %}
        {% site_url request.path %}
    """
    site_domain = getattr(settings, 'SITE_DOMAIN', None)
    if not site_domain:
        # Fallback for development (should not happen in production)
        site_domain = 'localhost'
    
    if path and not path.startswith('/'):
        path = '/' + path
    
    return f"https://{site_domain}{path}"

