"""
URL configuration for gr2quiz project.
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from quiz.sitemaps import SubjectListSitemap, SubjectSitemap, BlockSitemap, QuestionSitemap

# Sitemap configuration
sitemaps = {
    'subject-list': SubjectListSitemap,
    'subjects': SubjectSitemap,
    'blocks': BlockSitemap,
    'questions': QuestionSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('quiz.urls')),
    path('accounts/', include('quiz.auth_urls')),
]

