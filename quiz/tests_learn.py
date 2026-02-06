"""
Tests for public Learn/SEO pages.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question


class LearnPagesTestCase(TestCase):
    """Test public learn pages are accessible without authentication."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create a test question with answer and explanation
        self.question = Question.objects.create(
            subject='electrotehnica',
            qid=1,
            block_number=1,
            text='Test question text?',
            option_a='Option A',
            option_b='Option B',
            option_c='Option C',
            correct='a',
            explanation='This is a test explanation.'
        )
    
    def test_learn_subject_list_accessible(self):
        """Test that /learn/ returns 200 without authentication."""
        response = self.client.get('/learn/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Învață')
    
    def test_learn_subject_detail_accessible(self):
        """Test that subject detail page returns 200."""
        # Get subject slug
        from .utils import get_subject_slug
        slug = get_subject_slug('electrotehnica', 'Electrotehnică')
        response = self.client.get(f'/learn/{slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electrotehnică')
    
    def test_learn_block_detail_accessible(self):
        """Test that block detail page returns 200 and contains question."""
        from .utils import get_subject_slug, get_block_slug
        subject_slug = get_subject_slug('electrotehnica', 'Electrotehnică')
        block_slug = get_block_slug('electrotehnica', 1)
        response = self.client.get(f'/learn/{subject_slug}/{block_slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test question text?')
        self.assertContains(response, 'This is a test explanation.')
    
    def test_learn_question_detail_accessible(self):
        """Test that question detail page returns 200."""
        from .utils import get_subject_slug, get_block_slug
        subject_slug = get_subject_slug('electrotehnica', 'Electrotehnică')
        block_slug = get_block_slug('electrotehnica', 1)
        response = self.client.get(f'/learn/{subject_slug}/{block_slug}/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test question text?')
    
    def test_block_page_contains_question_text(self):
        """Test that block page contains at least one question text."""
        from .utils import get_subject_slug, get_block_slug
        subject_slug = get_subject_slug('electrotehnica', 'Electrotehnică')
        block_slug = get_block_slug('electrotehnica', 1)
        response = self.client.get(f'/learn/{subject_slug}/{block_slug}/')
        self.assertEqual(response.status_code, 200)
        # Check for question text
        self.assertContains(response, self.question.text)
    
    def test_block_page_contains_explanation(self):
        """Test that block page contains at least one explanation."""
        from .utils import get_subject_slug, get_block_slug
        subject_slug = get_subject_slug('electrotehnica', 'Electrotehnică')
        block_slug = get_block_slug('electrotehnica', 1)
        response = self.client.get(f'/learn/{subject_slug}/{block_slug}/')
        self.assertEqual(response.status_code, 200)
        # Check for explanation
        self.assertContains(response, self.question.explanation)


class SitemapTestCase(TestCase):
    """Test sitemap.xml generation."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        Question.objects.create(
            subject='electrotehnica',
            qid=1,
            block_number=1,
            text='Test question',
            option_a='A',
            option_b='B',
            option_c='C',
            correct='a',
            explanation='Test explanation'
        )
    
    def test_sitemap_returns_200(self):
        """Test that /sitemap.xml returns 200."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
    
    def test_sitemap_contains_learn_urls(self):
        """Test that sitemap contains at least one /learn/ URL."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('/learn/', content)


class RobotsTxtTestCase(TestCase):
    """Test robots.txt generation."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_robots_returns_200(self):
        """Test that /robots.txt returns 200."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')
    
    def test_robots_contains_sitemap(self):
        """Test that robots.txt contains 'Sitemap:' line."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Sitemap:', content)
    
    def test_robots_allows_learn(self):
        """Test that robots.txt allows /learn/."""
        response = self.client.get('/robots.txt')
        content = response.content.decode('utf-8')
        self.assertIn('Allow: /learn/', content)
    
    def test_robots_disallows_admin(self):
        """Test that robots.txt disallows /admin/."""
        response = self.client.get('/robots.txt')
        content = response.content.decode('utf-8')
        self.assertIn('Disallow: /admin/', content)

