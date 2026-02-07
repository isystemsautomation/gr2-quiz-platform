"""
Sitemap configuration for public learn pages.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Question
from .subjects import list_subjects
from .utils import get_subject_slug, get_block_slug


class SubjectSitemap(Sitemap):
    """Sitemap for subject list and detail pages."""
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        """Return all subjects."""
        subjects = list_subjects()
        return [(s['id'], s['title']) for s in subjects]
    
    def location(self, item):
        """Return URL for subject detail page."""
        subject_id, subject_title = item
        slug = get_subject_slug(subject_id, subject_title)
        return f'/learn/{slug}/'
    
    def lastmod(self, item):
        """Return last modification time based on questions in subject."""
        subject_id, _ = item
        latest_question = Question.objects.filter(subject=subject_id).order_by('-edited_at').first()
        if latest_question and latest_question.edited_at:
            return latest_question.edited_at
        return None


class SubjectListSitemap(Sitemap):
    """Sitemap for subject list page."""
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return [True]  # Single item for the list page
    
    def location(self, item):
        return '/learn/'


class BlockSitemap(Sitemap):
    """Sitemap for block detail pages."""
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        """Return all (subject_id, block_number) tuples."""
        blocks = Question.objects.values_list('subject', 'block_number').distinct()
        return list(blocks)
    
    def location(self, item):
        """Return URL for block detail page."""
        subject_id, block_number = item
        subject_info = next((s for s in list_subjects() if s['id'] == subject_id), None)
        if not subject_info:
            return '/learn/'  # Fallback to learn page
        subject_slug = get_subject_slug(subject_id, subject_info['title'])
        block_slug = get_block_slug(subject_id, block_number)
        return f'/learn/{subject_slug}/{block_slug}/'
    
    def lastmod(self, item):
        """Return last modification time for block."""
        subject_id, block_number = item
        latest_question = Question.objects.filter(
            subject=subject_id,
            block_number=block_number
        ).order_by('-edited_at').first()
        if latest_question and latest_question.edited_at:
            return latest_question.edited_at
        return None


class QuestionSitemap(Sitemap):
    """Sitemap for individual question pages."""
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        """Return all questions that have correct answer and explanation."""
        return Question.objects.filter(
            correct__isnull=False
        ).exclude(explanation='').select_related()
    
    def location(self, question):
        """Return URL for question detail page."""
        subject_info = next((s for s in _get_subjects_list() if s['id'] == question.subject), None)
        if not subject_info:
            return '/learn/'  # Fallback to learn page
        subject_slug = get_subject_slug(question.subject, subject_info['title'])
        block_slug = get_block_slug(question.subject, question.block_number)
        return f'/learn/{subject_slug}/{block_slug}/{question.qid}/'
    
    def lastmod(self, question):
        """Return last modification time for question."""
        return question.edited_at if question.edited_at else None

