"""
Public Learn/SEO views for quiz platform.
These views are accessible without authentication and are optimized for search engines.
"""
from django.shortcuts import render, get_object_or_404, Http404
from django.db.models import Prefetch
from django.utils.html import escape
import json

from .models import Question
from .utils import (
    get_subject_slug, get_block_slug, parse_subject_slug, parse_block_slug,
    get_question_image_url, get_option_image_url, build_absolute_https_url
)


def list_subjects():
    """Returns list of subject IDs and titles."""
    return [
        {'id': 'electrotehnica', 'title': 'Electrotehnică'},
        {'id': 'legislatie-gr-2', 'title': 'Legislație GR. 2'},
        {'id': 'norme-tehnice-gr-2', 'title': 'Norme Tehnice GR. 2'},
    ]


def learn_subject_list(request):
    """
    Public subject list page - shows all available subjects.
    URL: /learn/
    """
    subjects_data = []
    
    for subject_info in list_subjects():
        subject_id = subject_info['id']
        subject_title = subject_info['title']
        
        # Get block count for this subject
        block_count = Question.objects.filter(subject=subject_id).values_list('block_number', flat=True).distinct().count()
        
        # Get question count
        question_count = Question.objects.filter(subject=subject_id).count()
        
        subjects_data.append({
            'id': subject_id,
            'title': subject_title,
            'slug': get_subject_slug(subject_id, subject_title),
            'block_count': block_count,
            'question_count': question_count,
        })
    
    # Breadcrumb data
    breadcrumbs = [
        {'name': 'Acasă', 'url': '/'},
        {'name': 'Chestionare ANRE Grupa II', 'url': '/learn/'},
    ]
    
    # Structured data - BreadcrumbList (for backwards compatibility, but template has its own JSON-LD)
    structured_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Acasă",
                "item": "https://quiz.isystemsautomation.com/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Chestionare ANRE Grupa II",
                "item": "https://quiz.isystemsautomation.com/learn/"
            }
        ]
    }, ensure_ascii=False)
    
    return render(request, 'learn/subject_list.html', {
        'subjects': subjects_data,
        'breadcrumbs': breadcrumbs,
        'structured_data': structured_data,
    })


def learn_subject_detail(request, subject_slug):
    """
    Public subject detail page - shows all blocks for a subject.
    URL: /learn/<subject-slug>/
    """
    subject_id = parse_subject_slug(subject_slug)
    if not subject_id:
        raise Http404("Subject not found")
    
    # Get subject info
    subject_info = next((s for s in list_subjects() if s['id'] == subject_id), None)
    if not subject_info:
        raise Http404("Subject not found")
    
    subject_title = subject_info['title']
    
    # Get all blocks for this subject
    blocks = Question.objects.filter(subject=subject_id).values_list('block_number', flat=True).distinct().order_by('block_number')
    
    blocks_data = []
    for block_num in blocks:
        question_count = Question.objects.filter(subject=subject_id, block_number=block_num).count()
        blocks_data.append({
            'number': block_num,
            'slug': get_block_slug(subject_id, block_num),
            'question_count': question_count,
        })
    
    # Breadcrumb data
    breadcrumbs = [
        {'name': 'Acasă', 'url': '/'},
        {'name': 'Învață', 'url': '/learn/'},
        {'name': subject_title, 'url': f'/learn/{subject_slug}/'},
    ]
    
    # Structured data - BreadcrumbList
    structured_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Acasă",
                "item": request.build_absolute_uri('/')
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Învață",
                "item": request.build_absolute_uri('/learn/')
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": subject_title,
                "item": request.build_absolute_uri(f'/learn/{subject_slug}/')
            }
        ]
    }, ensure_ascii=False)
    
    return render(request, 'learn/subject_detail.html', {
        'subject': subject_info,
        'subject_slug': subject_slug,
        'blocks': blocks_data,
        'breadcrumbs': breadcrumbs,
        'structured_data': structured_data,
    })


def learn_block_detail(request, subject_slug, block_slug):
    """
    Public block detail page - shows all questions with answers and explanations.
    URL: /learn/<subject-slug>/<block-slug>/
    """
    subject_id, block_number = parse_block_slug(block_slug)
    if not subject_id or not block_number:
        raise Http404("Block not found")
    
    # Verify subject slug matches
    expected_subject_slug = get_subject_slug(subject_id, next((s['title'] for s in list_subjects() if s['id'] == subject_id), ''))
    if subject_slug != expected_subject_slug:
        raise Http404("Subject slug mismatch")
    
    # Get subject info
    subject_info = next((s for s in list_subjects() if s['id'] == subject_id), None)
    if not subject_info:
        raise Http404("Subject not found")
    
    # Get all questions for this block
    questions = Question.objects.filter(
        subject=subject_id,
        block_number=block_number
    ).order_by('qid')
    
    if not questions.exists():
        raise Http404("Block not found")
    
    # Prepare questions data with images
    questions_data = []
    for question in questions:
        question_img_exists, question_img_url = get_question_image_url(question, subject_id)
        option_a_exists, option_a_url = get_option_image_url(question, subject_id, 1)
        option_b_exists, option_b_url = get_option_image_url(question, subject_id, 2)
        option_c_exists, option_c_url = get_option_image_url(question, subject_id, 3)
        
        questions_data.append({
            'question': question,
            'question_img_exists': question_img_exists,
            'question_img_url': question_img_url,
            'option_a_exists': option_a_exists,
            'option_a_url': option_a_url,
            'option_b_exists': option_b_exists,
            'option_b_url': option_b_url,
            'option_c_exists': option_c_exists,
            'option_c_url': option_c_url,
        })
    
    # Breadcrumb data (absolute HTTPS URLs)
    breadcrumbs = [
        {'name': 'Acasă', 'url': home_url},
        {'name': 'Învață', 'url': learn_url},
        {'name': subject_info['title'], 'url': subject_url},
        {'name': f'Bloc {block_number}', 'url': block_url},
    ]
    
    # Build absolute HTTPS URLs
    base_url = build_absolute_https_url(request)
    home_url = build_absolute_https_url(request, '/')
    learn_url = build_absolute_https_url(request, '/learn/')
    subject_url = build_absolute_https_url(request, f'/learn/{subject_slug}/')
    block_url = build_absolute_https_url(request, f'/learn/{subject_slug}/{block_slug}/')
    
    # Structured data - BreadcrumbList
    breadcrumb_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Acasă",
                "item": home_url
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Învață",
                "item": learn_url
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": subject_info['title'],
                "item": subject_url
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": f"Bloc {block_number}",
                "item": block_url
            }
        ]
    }, ensure_ascii=False)
    
    # Structured data - ItemList (question permalinks)
    item_list_items = []
    for idx, item in enumerate(questions_data, 1):
        question = item['question']
        question_url = build_absolute_https_url(request, f'/learn/{subject_slug}/{block_slug}/{question.qid}/')
        item_list_items.append({
            "@type": "ListItem",
            "position": idx,
            "item": {
                "@type": "Question",
                "name": question.text[:100] + "..." if len(question.text) > 100 else question.text,
                "url": question_url
            }
        })
    
    item_list_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{subject_info['title']} - Bloc {block_number}",
        "numberOfItems": len(item_list_items),
        "itemListElement": item_list_items
    }, ensure_ascii=False)
    
    structured_data = [breadcrumb_data, item_list_data]
    
    # Canonical URL (absolute HTTPS)
    canonical_url = block_url
    
    return render(request, 'learn/block_detail.html', {
        'subject': subject_info,
        'subject_slug': subject_slug,
        'block_number': block_number,
        'block_slug': block_slug,
        'questions': questions_data,
        'breadcrumbs': breadcrumbs,
        'structured_data': structured_data,
        'canonical_url': canonical_url,
    })


def learn_question_detail(request, subject_slug, block_slug, question_id):
    """
    Public question detail page - shows a single question with answer and explanation.
    URL: /learn/<subject-slug>/<block-slug>/<question-id>/
    """
    subject_id, block_number = parse_block_slug(block_slug)
    if not subject_id or not block_number:
        raise Http404("Block not found")
    
    # Verify subject slug matches
    expected_subject_slug = get_subject_slug(subject_id, next((s['title'] for s in list_subjects() if s['id'] == subject_id), ''))
    if subject_slug != expected_subject_slug:
        raise Http404("Subject slug mismatch")
    
    # Get subject info
    subject_info = next((s for s in list_subjects() if s['id'] == subject_id), None)
    if not subject_info:
        raise Http404("Subject not found")
    
    # Get the question
    try:
        question = Question.objects.get(
            subject=subject_id,
            block_number=block_number,
            qid=question_id
        )
    except Question.DoesNotExist:
        raise Http404("Question not found")
    
    # Get images
    question_img_exists, question_img_url = get_question_image_url(question, subject_id)
    option_a_exists, option_a_url = get_option_image_url(question, subject_id, 1)
    option_b_exists, option_b_url = get_option_image_url(question, subject_id, 2)
    option_c_exists, option_c_url = get_option_image_url(question, subject_id, 3)
    
    # Breadcrumb data
    breadcrumbs = [
        {'name': 'Acasă', 'url': '/'},
        {'name': 'Învață', 'url': '/learn/'},
        {'name': subject_info['title'], 'url': f'/learn/{subject_slug}/'},
        {'name': f'Bloc {block_number}', 'url': f'/learn/{subject_slug}/{block_slug}/'},
        {'name': f'Întrebarea {question_id}', 'url': f'/learn/{subject_slug}/{block_slug}/{question_id}/'},
    ]
    
    # Structured data - BreadcrumbList
    structured_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Acasă",
                "item": request.build_absolute_uri('/')
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Învață",
                "item": request.build_absolute_uri('/learn/')
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": subject_info['title'],
                "item": request.build_absolute_uri(f'/learn/{subject_slug}/')
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": f"Bloc {block_number}",
                "item": request.build_absolute_uri(f'/learn/{subject_slug}/{block_slug}/')
            },
            {
                "@type": "ListItem",
                "position": 5,
                "name": f"Întrebarea {question_id}",
                "item": request.build_absolute_uri(f'/learn/{subject_slug}/{block_slug}/{question_id}/')
            }
        ]
    }, ensure_ascii=False)
    
    return render(request, 'learn/question_detail.html', {
        'subject': subject_info,
        'subject_slug': subject_slug,
        'block_number': block_number,
        'block_slug': block_slug,
        'question': question,
        'question_id': question_id,
        'question_img_exists': question_img_exists,
        'question_img_url': question_img_url,
        'option_a_exists': option_a_exists,
        'option_a_url': option_a_url,
        'option_b_exists': option_b_exists,
        'option_b_url': option_b_url,
        'option_c_exists': option_c_exists,
        'option_c_url': option_c_url,
        'breadcrumbs': breadcrumbs,
        'structured_data': structured_data,
    })

