import os

import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Scripts

CONTENT_CREATOR_GROUP = 'Content Creator'
OPENAI_URL = 'https://api.openai.com/v1/chat/completions'


@login_required
def index(request):
    user = request.user
    if not user.groups.filter(name=CONTENT_CREATOR_GROUP).exists():
        return redirect('scripts')

    scripts = Scripts.objects.filter(user=user)
    return render(request, 'index.html', {'scripts': scripts, 'user': user})


@login_required
def scripts(request):
    scripts = Scripts.objects.all()
    return render(request, 'scripts.html', {'scripts': scripts})


def validate_custom_password(password):
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")
    if not any(not char.isalnum() for char in password):
        raise ValidationError("Password must contain at least one special character.")
    validate_password(password)


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not password1:
            messages.error(request, "Username and password are required")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if any(c.isupper() for c in username):
            messages.error(request, "Username should not contain uppercase characters")
            return redirect('signup')

        try:
            validate_custom_password(password1)
        except ValidationError as validation_errors:
            for error in validation_errors:
                messages.error(request, error)
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password1)

        auth_user = authenticate(request, username=username, password=password1)
        login(request, auth_user)

        return redirect('index')

    return render(request, 'signup.html')


def login_user(request):
    if request.method == 'POST':
        username_email = request.POST.get('username_email', '').strip()
        password = request.POST.get('password', '')

        # Allow signing in with an email address as well as a username
        username = username_email
        if '@' in username_email:
            match = User.objects.filter(email__iexact=username_email).first()
            if match:
                username = match.username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username/email or password')
            return redirect('login')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def call_openai(prompt, max_tokens):
    """Send a prompt to OpenAI and return the reply text, or None on failure."""
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return None

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'),
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens
    }
    try:
        response = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=60)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None
    return response.json()['choices'][0]['message']['content'].strip()


@login_required
@require_POST
def generate_script(request):
    title = request.POST.get('title')
    idea = request.POST.get('idea')

    if not title or not idea:
        return JsonResponse({'error': 'Please enter title and idea.'})

    generated_script = generate_script_using_openai(title, idea)

    if generated_script:
        script = Scripts(title=title, idea=idea, generated_script=generated_script, user=request.user)
        script.save()
        return JsonResponse({'message': 'Script generated successfully'})
    else:
        return JsonResponse({'error': 'Failed to generate script.'})


def generate_script_using_openai(title, idea):
    prompt = f'Title: {title}\nIdea: {idea}\nGenerate script:'
    return call_openai(prompt, max_tokens=1000)


@login_required
def get_script(request, script_id):
    try:
        script = Scripts.objects.get(pk=script_id)
        return JsonResponse({'script': script.generated_script})
    except Scripts.DoesNotExist:
        return JsonResponse({'script': 'Script not found'}, status=404)


@login_required
@require_POST
def edit_script(request, script_id):
    script = get_object_or_404(Scripts, pk=script_id, user=request.user)

    updated_script = request.POST.get('generated_script')
    updated_quiz = request.POST.get('quiz', '')

    if not updated_script:
        return JsonResponse({'error': 'Invalid script data'})

    script.generated_script = updated_script
    script.quiz = updated_quiz
    script.save()

    return JsonResponse({'message': 'Script updated successfully'})


@login_required
@require_POST
def delete_script(request, script_id):
    script = get_object_or_404(Scripts, pk=script_id, user=request.user)
    script.delete()
    return JsonResponse({'message': 'Script deleted successfully'})


@login_required
@require_POST
def generate_quiz(request):
    script_id = request.POST.get('script_id')
    title = request.POST.get('title')
    generated_script = request.POST.get('generated_script')

    if not script_id or not title or not generated_script:
        return JsonResponse({'error': 'Please provide the script ID, title, and generated script.'}, status=400)

    script = get_object_or_404(Scripts, pk=script_id, user=request.user)

    quiz = generate_quiz_using_openai(title, generated_script)

    if quiz:
        script.quiz = quiz
        script.save()
        return JsonResponse({'message': 'Quiz generated successfully', 'quiz': quiz})
    else:
        return JsonResponse({'error': 'Failed to generate quiz.'}, status=500)


def generate_quiz_using_openai(title, generated_script):
    prompt = f'Title: {title}\nGenerated Script: {generated_script}\nGenerate 1 MCQ quiz questions and specify the heading for choices as "choices" and also correct answer \n'
    return call_openai(prompt, max_tokens=300)


@login_required
@require_POST
def get_generated_quiz(request):
    title = request.POST.get('title')
    generated_script = request.POST.get('generated_script')

    if not title or not generated_script:
        return JsonResponse({'error': 'Please enter title and generated script.'})

    quiz = generate_quiz_using_openai(title, generated_script)

    if quiz:
        return JsonResponse({'quiz': quiz})
    else:
        return JsonResponse({'error': 'Failed to generate quiz.'}, status=500)
