"""
Middleware to enforce authentication on all routes except login/register/static.
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class AuthenticationRequiredMiddleware:
    """
    Middleware that requires authentication for all views except:
    - /accounts/login/
    - /accounts/register/
    - /accounts/logout/ (POST only)
    - Static files
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [
            '/accounts/login/',
            '/accounts/register/',
            '/static/',
        ]
        # Public paths that don't require authentication
        self.public_paths = [
            '/learn/',
            '/sitemap.xml',
            '/robots.txt',
        ]

    def __call__(self, request):
        # Allow static files
        if request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Allow login and register pages
        if request.path in self.exempt_paths:
            return self.get_response(request)
        
        # Allow public learn pages, sitemap, and robots.txt
        if request.path.startswith('/learn/') or request.path in ['/sitemap.xml', '/robots.txt']:
            return self.get_response(request)
        
        # Allow logout (GET or POST)
        if request.path == '/accounts/logout/':
            return self.get_response(request)
        
        # Require authentication for all other paths
        if not request.user.is_authenticated:
            return redirect('login')
        
        return self.get_response(request)

