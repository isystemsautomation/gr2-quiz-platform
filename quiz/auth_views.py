from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .rate_limit import rate_limit


@rate_limit(max_attempts=5, window_seconds=300, key_prefix='login')
def login_view(request):
    """Login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Rate limit counter will be reset by decorator
            return redirect('dashboard')
        else:
            # Failed login - rate limit counter already incremented
            return render(request, 'registration/login.html', {
                'error': 'Invalid username or password.',
            })
    
    return render(request, 'registration/login.html')


@rate_limit(max_attempts=3, window_seconds=600, key_prefix='register')
def register_view(request):
    """Registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Rate limit counter will be reset by decorator
            return redirect('dashboard')
        # Invalid form - rate limit counter already incremented
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def logout_view(request):
    """Logout view."""
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')
