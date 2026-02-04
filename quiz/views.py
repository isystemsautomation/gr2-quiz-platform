from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from .models import BlockAttempt
from .loader import list_subjects, get_blocks, get_block_questions


def index(request):
    """Redirect to dashboard if authenticated, else to login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    """Display dashboard with all subjects and blocks."""
    subjects_data = []
    
    for subject_info in list_subjects():
        subject_id = subject_info['id']
        subject_title = subject_info['title']
        blocks = get_blocks(subject_id)
        
        # Get last attempt for each block
        block_data = []
        for block_num in blocks:
            last_attempt = BlockAttempt.objects.filter(
                user=request.user,
                subject=subject_id,
                block_number=block_num
            ).order_by('-taken_at').first()
            
            # Determine color class based on last attempt
            if last_attempt:
                if last_attempt.score == last_attempt.total:
                    color_class = 'block-green'
                elif last_attempt.score >= last_attempt.total - 2:
                    color_class = 'block-yellow'
                else:
                    color_class = 'block-red'
            else:
                color_class = 'block-white'
            
            block_data.append({
                'number': block_num,
                'last_attempt': last_attempt,
                'color_class': color_class,
            })
        
        subjects_data.append({
            'id': subject_id,
            'title': subject_title,
            'blocks': block_data,
        })
    
    return render(request, 'quiz/dashboard.html', {
        'subjects': subjects_data,
    })


@login_required
def block_take(request, subject, block_number):
    """Display questions for a specific block."""
    # Validate subject
    valid_subjects = [s['id'] for s in list_subjects()]
    if subject not in valid_subjects:
        raise Http404("Subject not found")
    
    # Get questions for this block
    questions = get_block_questions(subject, block_number)
    
    if not questions:
        raise Http404("Block not found")
    
    # Get subject title
    subject_title = next(
        (s['title'] for s in list_subjects() if s['id'] == subject),
        subject
    )
    
    return render(request, 'quiz/block_take.html', {
        'subject': subject,
        'subject_title': subject_title,
        'block_number': block_number,
        'questions': questions,
    })


@login_required
@require_http_methods(["POST"])
def block_submit(request, subject, block_number):
    """Grade and save quiz attempt."""
    # Validate subject
    valid_subjects = [s['id'] for s in list_subjects()]
    if subject not in valid_subjects:
        raise Http404("Subject not found")
    
    # Get questions for this block
    questions = get_block_questions(subject, block_number)
    
    if not questions:
        raise Http404("Block not found")
    
    # Grade the quiz
    score = 0
    total_gradable = 0
    results = []
    
    for question in questions:
        q_id = str(question['id'])
        user_answer = request.POST.get(f'question_{q_id}')
        correct_answer = question.get('correct')
        
        # Skip ungradable questions (correct is null)
        if correct_answer is None:
            results.append({
                'question': question,
                'user_answer': user_answer,
                'correct_answer': None,
                'is_correct': None,
                'explanation': question.get('explanation', ''),
            })
            continue
        
        total_gradable += 1
        is_correct = user_answer == correct_answer
        
        if is_correct:
            score += 1
        
        results.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'explanation': question.get('explanation', ''),
        })
    
    # Calculate percentage
    percentage = (score / total_gradable * 100) if total_gradable > 0 else 0.0
    
    # Save attempt
    attempt = BlockAttempt.objects.create(
        user=request.user,
        subject=subject,
        block_number=block_number,
        score=score,
        total=total_gradable,
        percentage=percentage,
    )
    
    # Get subject title
    subject_title = next(
        (s['title'] for s in list_subjects() if s['id'] == subject),
        subject
    )
    
    return render(request, 'quiz/block_result.html', {
        'subject': subject,
        'subject_title': subject_title,
        'block_number': block_number,
        'attempt': attempt,
        'results': results,
    })

