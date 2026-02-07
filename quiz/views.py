from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Q
from django.utils import timezone
from django.contrib import messages

from .models import BlockAttempt, Question, BlockNote
from .utils import get_question_image_url, get_option_image_url


def index(request):
    """Redirect to dashboard if authenticated, else to login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def list_subjects():
    """Returns list of subject IDs and titles."""
    return [
        {'id': 'electrotehnica', 'title': 'Electrotehnică'},
        {'id': 'legislatie-gr-2', 'title': 'Legislație GR. 2'},
        {'id': 'norme-tehnice-gr-2', 'title': 'Norme Tehnice GR. 2'},
    ]


@login_required
def dashboard(request):
    """Display dashboard with all subjects and blocks."""
    subjects_data = []
    
    for subject_info in list_subjects():
        subject_id = subject_info['id']
        subject_title = subject_info['title']
        
        # Get blocks from database
        blocks = Question.objects.filter(subject=subject_id).values_list('block_number', flat=True).distinct().order_by('block_number')

        # Personal notes for this subject / user, indexed by block number
        notes_qs = BlockNote.objects.filter(user=request.user, subject=subject_id)
        notes_by_block = {n.block_number: n.note for n in notes_qs}
        
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
                'note': notes_by_block.get(block_num, ""),
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
    
    # Get questions for this block from database
    questions = Question.objects.filter(
        subject=subject,
        block_number=block_number
    ).order_by('qid')
    
    if not questions.exists():
        raise Http404("Block not found")
    
    # Get subject title
    subject_title = next(
        (s['title'] for s in list_subjects() if s['id'] == subject),
        subject
    )
    
    # Personal note for this block (per user)
    note_obj = BlockNote.objects.filter(
        user=request.user,
        subject=subject,
        block_number=block_number,
    ).first()
    block_note = note_obj.note if note_obj else ""

    # Prepare questions with image URLs
    questions_data = []
    for question in questions:
        # Check if question can be edited by this user
        has_answer = bool(question.correct)
        has_explanation = bool(question.explanation and question.explanation.strip())
        can_edit = (not has_answer or not has_explanation) or request.user.is_superuser
        
        # Get image URLs
        question_img_exists, question_img_url = get_question_image_url(question, subject)
        option_a_exists, option_a_url = get_option_image_url(question, subject, 1)
        option_b_exists, option_b_url = get_option_image_url(question, subject, 2)
        option_c_exists, option_c_url = get_option_image_url(question, subject, 3)
        
        questions_data.append({
            'question': question,
            'can_edit': can_edit,
            'has_answer': has_answer,
            'has_explanation': has_explanation,
            'question_img_exists': question_img_exists,
            'question_img_url': question_img_url,
            'option_a_exists': option_a_exists,
            'option_a_url': option_a_url,
            'option_b_exists': option_b_exists,
            'option_b_url': option_b_url,
            'option_c_exists': option_c_exists,
            'option_c_url': option_c_url,
        })
    
    return render(request, 'quiz/block_take.html', {
        'subject': subject,
        'subject_title': subject_title,
        'block_number': block_number,
        'questions': questions_data,
        'block_note': block_note,
    })


@login_required
@require_http_methods(["POST"])
def block_submit(request, subject, block_number):
    """Grade and save quiz attempt."""
    # Validate subject
    valid_subjects = [s['id'] for s in list_subjects()]
    if subject not in valid_subjects:
        raise Http404("Subject not found")
    
    # Get questions for this block from database
    questions = Question.objects.filter(
        subject=subject,
        block_number=block_number
    ).order_by('qid')
    
    if not questions.exists():
        raise Http404("Block not found")
    
    # Grade the quiz
    score = 0
    total_gradable = 0
    results = []
    
    for question in questions:
        q_id = str(question.qid)
        user_answer = request.POST.get(f'question_{q_id}')
        correct_answer = question.correct
        
        # Skip ungradable questions (correct is null)
        if correct_answer is None:
            results.append({
                'question': question,
                'user_answer': user_answer,
                'correct_answer': None,
                'is_correct': None,
                'explanation': question.explanation,
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
            'explanation': question.explanation,
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
        'block_note': BlockNote.objects.filter(
            user=request.user,
            subject=subject,
            block_number=block_number,
        ).first(),
    })


@login_required
def question_edit(request, pk):
    """Edit a question (for normal users to fill missing data, or superuser to edit anything)."""
    question = get_object_or_404(Question, pk=pk)
    
    # Check if user can edit
    can_edit = (not question.correct or not question.explanation) or request.user.is_superuser
    if not can_edit:
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Optimistic locking: prevent overwriting newer edits
        posted_version = request.POST.get('version', '')
        current_version = question.edited_at.isoformat() if question.edited_at else ''
        if posted_version and posted_version != current_version and not request.user.is_superuser:
            messages.error(request, "Întrebarea a fost modificată între timp de un alt utilizator. Te rugăm să reîncarci pagina înainte de a salva din nou.")
            return redirect('question_edit', pk=question.pk)

        # Update question with server-side validation
        correct_val = request.POST.get('correct', '').strip()
        
        # Validate correct answer value (must be 'a', 'b', 'c', or empty)
        if correct_val and correct_val not in ['a', 'b', 'c']:
            messages.error(request, "Răspunsul corect trebuie să fie 'a', 'b' sau 'c'.")
            return redirect('question_edit', pk=question.pk)
        
        if not question.correct and correct_val:
            # Normal user: can only set if currently empty
            question.correct = correct_val
        elif request.user.is_superuser:
            # Superuser can set or clear correct answer
            question.correct = correct_val if correct_val else None
        
        if not question.explanation and request.POST.get('explanation'):
            question.explanation = request.POST.get('explanation', '')
        elif request.user.is_superuser:
            question.explanation = request.POST.get('explanation', '')
        
        if request.user.is_superuser:
            question.image_base = request.POST.get('image_base', '').strip()
        
        question.edited_by = request.user
        question.edited_at = timezone.now()
        question.save()
        
        # Redirect back to block page or dashboard
        redirect_to = request.GET.get('next', 'dashboard')
        if redirect_to == 'block':
            # Redirect to block page with anchor to the specific question
            from django.urls import reverse
            block_url = reverse('block_take', kwargs={
                'subject': question.subject,
                'block_number': question.block_number
            })
            return redirect(f'{block_url}#question-{question.pk}')
        return redirect('dashboard')
    
    # GET request - show edit form
    return render(request, 'quiz/question_edit.html', {
        'question': question,
        'subject': question.subject,
        'version': question.edited_at.isoformat() if question.edited_at else '',
    })


@login_required
@require_http_methods(["POST"])
def block_note_save(request, subject, block_number):
    """Save or update personal note for a block (per user)."""
    # Validate subject
    valid_subjects = [s['id'] for s in list_subjects()]
    if subject not in valid_subjects:
        raise Http404("Subject not found")

    note_text = request.POST.get('note', '').strip()

    note_obj, _ = BlockNote.objects.get_or_create(
        user=request.user,
        subject=subject,
        block_number=block_number,
    )
    note_obj.note = note_text
    note_obj.save()

    messages.success(request, "Nota pentru acest bloc a fost salvată.")
    # Redirect back to block page
    return redirect('block_take', subject=subject, block_number=block_number)

