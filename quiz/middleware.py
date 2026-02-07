"""
Middleware to enforce authentication on all routes except login/register/static.
"""
from django.shortcuts import redirect


class AuthenticationRequiredMiddleware:
    """
    Middleware that requires authentication for all views except:
    - /accounts/login/
    - /accounts/register/
    - /accounts/logout/ (POST only, enforced by view decorator)
    - Static files
    - Public learn pages (/learn/)
    - SEO routes (/sitemap.xml, /robots.txt, /LICENSE)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that don't require authentication
        self.exempt_paths = [
            '/accounts/login/',
            '/accounts/register/',
            '/static/',
            '/learn/',
            '/sitemap.xml',
            '/robots.txt',
            '/LICENSE',
        ]

    def __call__(self, request):
        # Allow static files
        if request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Allow exempt paths (login, register, public learn pages, SEO routes)
        if request.path in self.exempt_paths:
            return self.get_response(request)
        
        # Allow paths that start with exempt prefixes
        if any(request.path.startswith(path) for path in self.exempt_paths if path.endswith('/')):
            return self.get_response(request)
        
        # Require authentication for all other paths
        if not request.user.is_authenticated:
            return redirect('login')
        
        return self.get_response(request)

