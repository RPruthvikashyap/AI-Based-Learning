from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Scripts
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django_auth_ldap.backend import LDAPBackend

@login_required
def index(request):
    user = request.user
    content_creator_group = Group.objects.get(name='Content Creator')
    if not user.groups.filter(name=content_creator_group).exists():
        return redirect('scripts')

    scripts = Scripts.objects.filter(user=user)
    return render(request, 'index.html', {'scripts': scripts, 'user': user})

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
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        try:
            User.objects.get(username=username)
            messages.error(request, "Username already exists")
            return redirect('signup')
        except User.DoesNotExist:
            pass

        if any(c.isupper() for c in username):
            messages.error(request, "Username should not contain uppercase characters")
            return redirect('signup')

        try:
            validate_custom_password(password1)
        except ValidationError as validation_errors:
            for error in validation_errors:
                messages.error(request, error)
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        auth_user = authenticate(username=username, password=password1)
        login(request, auth_user)

        return redirect('index')

    return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        username_email = request.POST.get('username_email')
        password = request.POST.get('password')
        ldap_backend = LDAPBackend()
        user = ldap_backend.authenticate(request, username=username_email, password=password)

        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username/email or password')
            return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect("index")

def generate_script(request):
    if request.method == 'POST':
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
    api_key = 'Enter Your openAI API'
    url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'
    prompt = f'Title: {title}\nIdea: {idea}\nGenerate script:'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': prompt,
        'max_tokens': 1000
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        generated_script = data['choices'][0]['text'].strip()
        return generated_script
    else:
        return None

def get_script(request, script_id):
    try:
        script = Scripts.objects.get(pk=script_id)
        return JsonResponse({'script': script.generated_script})
    except Scripts.DoesNotExist:
        return JsonResponse({'script': 'Script not found'}, status=404)

@csrf_exempt
@csrf_exempt
def edit_script(request, script_id):
    if request.method == 'POST':
        try:
            script = Scripts.objects.get(pk=script_id)
        except Scripts.DoesNotExist:
            return JsonResponse({'error': 'Script not found'}, status=404)

        updated_script = request.POST.get('generated_script')
        updated_quiz = request.POST.get('quiz') 

        if not updated_script:
            return JsonResponse({'error': 'Invalid script data'})

        script.generated_script = updated_script
        script.quiz = updated_quiz 
        script.save()

        return JsonResponse({'message': 'Script updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_script(request, script_id):
    try:
        script = Scripts.objects.get(pk=script_id)
    except Scripts.DoesNotExist:
        return JsonResponse({'error': 'Script not found'}, status=404)

    if request.method == 'POST':
        script.delete()
        return JsonResponse({'message': 'Script deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
from django.http import JsonResponse

def generate_quiz(request):
    if request.method == 'POST':
        script_id = request.POST.get('script_id')  # Add this line to get the script ID from the request
        title = request.POST.get('title')
        generated_script = request.POST.get('generated_script')

        if not script_id or not title or not generated_script:
            return JsonResponse({'error': 'Please provide the script ID, title, and generated script.'}, status=400)

        try:
            script = Scripts.objects.get(pk=script_id)
        except Scripts.DoesNotExist:
            return JsonResponse({'error': 'Script not found'}, status=404)

        quiz = generate_quiz_using_openai(title, generated_script)

        if quiz:
            try:
                script.quiz = quiz  
                script.save()
            except Exception as e:
                return JsonResponse({'error': f'Failed to save the generated quiz: {e}'}, status=500)

            return JsonResponse({'message': 'Quiz generated successfully', 'quiz': quiz})
        else:
            return JsonResponse({'error': 'Failed to generate quiz.'}, status=500)

def generate_quiz_using_openai(title, generated_script):
    api_key = 'ENter Your openAI API'
    url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'

    prompt = f'Title: {title}\nGenerated Script: {generated_script}\nGenerate 1 MCQ quiz questions and specify the heading for choices as "choices" and also correct answer \n'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': prompt,
        'max_tokens': 300
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        generated_quiz = data['choices'][0]['text'].strip()
        return generated_quiz
    else:
        return None

from django.http import JsonResponse

def get_generated_quiz(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        generated_script = request.POST.get('generated_script')

        if not title or not generated_script:
            return JsonResponse({'error': 'Please enter title and generated script.'})

        quiz = generate_quiz_using_openai(title, generated_script)

        if quiz:
            return JsonResponse({'quiz': quiz})
        else:
            return JsonResponse({'error': 'Failed to generate quiz.'}, status=500)
