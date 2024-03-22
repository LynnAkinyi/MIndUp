from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Article
from .models import MindfulnessTask, ExerciseTask
from .models import Profile
from django.views.decorators.http import require_POST
from .forms import ProfileForm


def tasks(request):
    mindfulness_task = MindfulnessTask.objects.get_or_create()[0]
    exercise_task = ExerciseTask.objects.get_or_create()[0]

    context = {
        'mindfulness_task': mindfulness_task,
        'exercise_task': exercise_task,
    }
    return render(request, 'tasks.html', context)

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def book(request):
    return render(request, 'book.html')

def chat(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'chat.html', {'users': users})


def create_article(request):
    return render(request, 'create_article.html')

def save_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title, content=content)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def details(request):
    return render(request, 'details.html')


def dir(request):
    return render(request, 'dir.html')


def faq(request):
    return render(request, 'faq.html')


def testimonies(request):
    return render(request, 'testimonies.html')


def forums(request):
    return render(request, 'forums.html')

def contact(request):
    return render(request, 'contact.html')


@login_required
def community(request):
    return render(request, 'community.html')

@login_required
def blog(request):
    return render(request, 'blog.html')

def about(request):
    return render(request, 'about.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_staff:
                    login(request, user)
                    return redirect('http://127.0.0.1:8000/admin/login/?next=/admin/')
                else:
                    login(request, user)
                    return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
# logout page
def user_logout(request):
    logout(request)
    return redirect('home')

def schedule_appointment(request):
    if request.method == 'POST':
        selected_date = request.POST.get('appointment_date')
        if selected_date:
            # Perform any necessary operations, such as saving to the database
            # Here, we'll just redirect to the dashboard with the selected date
            return redirect('dashboard', appointment_date=selected_date)
    return redirect('book')

def forums(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'forums.html', {'users': users})

@csrf_exempt
def user_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        # Here you can save the user details to the database or perform any other necessary actions
        # For simplicity, let's just return the user details as JSON response
        return JsonResponse({'name': name, 'email': email})
    else:
        # Handle GET requests or any other methods if needed
        pass

def create_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')
        Article.objects.create(title=title, content=content, image=image)
        return redirect('article_list')
    return render(request, 'create_article.html')

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    article.delete()
    return redirect('article_list')

def view_all_therapists(request):
    therapists = Profile.objects.filter(role='therapist')
    return render(request, 'dir.html', {'therapists': therapists})


@login_required
@csrf_exempt
def save_profile(request):
    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.name = request.POST.get('name')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.role = request.POST.get('role')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'bad request'}, status=400)
    
    
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            if profile.role == 'therapist':
                return redirect('view_all_therapists')
            else:  # profile.role == 'member'
                return redirect('dashboard')

    return render(request, 'profile.html', {'form': ProfileForm})

def view_all_therapists(request):
    therapists = Profile.objects.filter(role='therapist')
    return render(request, 'dir.html', {'therapists': therapists})

def forums(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'forums.html', {'profile': profile})
