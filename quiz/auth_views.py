from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


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
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid username or password.',
            })
    
    return render(request, 'registration/login.html')


def register_view(request):
    """Registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Logout view."""
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

