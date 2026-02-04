"""
URL configuration for gr2quiz project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path('accounts/', include('quiz.auth_urls')),
]

