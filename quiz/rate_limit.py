"""
Rate limiting decorators for authentication endpoints.
Prevents brute-force attacks on login and registration.
"""
from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings
import time


def rate_limit(max_attempts=5, window_seconds=300, key_prefix='rate_limit'):
    """
    Rate limiting decorator for authentication endpoints.
    Only counts failed attempts (not successful ones).
    
    Args:
        max_attempts: Maximum number of failed attempts allowed
        window_seconds: Time window in seconds (default: 5 minutes)
        key_prefix: Prefix for cache key
    
    Returns:
        Decorated function that enforces rate limiting
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get client identifier (IP address)
            # Security: Only trust X-Forwarded-For if we're behind a known proxy
            # Otherwise use REMOTE_ADDR to prevent spoofing
            use_forwarded = getattr(settings, 'DJANGO_USE_X_FORWARDED_PROTO', False)
            if use_forwarded:
                # Behind proxy - trust first IP in X-Forwarded-For (proxy should sanitize)
                forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
                if forwarded:
                    client_ip = forwarded.split(',')[0].strip()
                else:
                    client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            else:
                # Direct connection - use REMOTE_ADDR (cannot be spoofed)
                client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            
            # Build cache key
            cache_key = f"{key_prefix}:{client_ip}"
            
            # Get current failed attempts
            attempts_data = cache.get(cache_key, {'count': 0, 'first_attempt': time.time()})
            
            # Check if window has expired
            elapsed = time.time() - attempts_data['first_attempt']
            if elapsed > window_seconds:
                # Reset window
                attempts_data = {'count': 0, 'first_attempt': time.time()}
            
            # Check if limit exceeded (only for POST requests)
            if request.method == 'POST' and attempts_data['count'] >= max_attempts:
                remaining = int(window_seconds - elapsed)
                return HttpResponse(
                    f"Prea multe încercări eșuate. Te rugăm să încerci din nou în {remaining} secunde.",
                    status=429,
                    content_type='text/plain; charset=utf-8'
                )
            
            # Call the view
            response = view_func(request, *args, **kwargs)
            
            # Only count failed attempts (POST requests that didn't result in authentication)
            if request.method == 'POST':
                # Check if authentication was successful
                is_successful = False
                if hasattr(response, 'status_code'):
                    # Successful login/registration results in redirect (302) with authenticated user
                    if response.status_code == 302:
                        # Check if user is authenticated after the view
                        # Note: login() sets user in request, so we check after view execution
                        if request.user.is_authenticated:
                            is_successful = True
                
                if is_successful:
                    # Successful authentication - reset counter
                    cache.delete(cache_key)
                else:
                    # Failed attempt - increment counter
                    attempts_data['count'] += 1
                    cache.set(cache_key, attempts_data, window_seconds)
            
            return response
        
        return wrapper
    return decorator

