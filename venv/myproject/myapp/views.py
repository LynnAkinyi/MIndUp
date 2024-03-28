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
from .forms import ArticleForm
from .models import MindfulnessTask, ExerciseTask
from .models import Profile
from django.views.decorators.http import require_POST
from .forms import ProfileForm, TestimoniesForm
from .models import Article, Group, Therapist, Testimonies, Appointment
import base64
import uuid
from django.core.files.base import ContentFile
from django.views import View
from django.http import HttpResponse



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
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile')
    
    articles = Article.objects.all().order_by('-date')     # get all articles
    context = {'role': profile.role, 'articles': articles}  # add articles to the context
    
    return render(request, 'dashboard.html', context)

def book(request, therapist_id=None):
    if therapist_id is not None:
        therapist = Therapist.objects.get(id=therapist_id)
    else:
        therapist = None
    return render(request, 'book.html', {'therapist': therapist})

def chat(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'chat.html', {'users': users})

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()  # Save the form and get the article instance
            return redirect('blog')  # Redirect to the blog page
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})

def save_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title, content=content)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def details(request):
    return render(request, 'details.html')

def read(request):
    articles = Article.objects.order_by('-date')  # Order articles by date in descending order
    return render(request, 'read.html', {'articles': articles})

def faq(request):
    return render(request, 'faq.html')


def testimonies(request):
    return render(request, 'testimonies.html')


def forums(request):
    groups = Group.objects.all()
    volunteers = Volunteer.objects.all()
    return render(request, 'forums.html', {'groups': groups, 'volunteers': volunteers})

def get_groups(request):
    groups = Group.objects.all().values_list('name', flat=True)
    return JsonResponse({'groups': list(groups)})
@csrf_exempt
def save_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_name = data.get('name')
        if group_name:
            group = Group(name=group_name)
            group.save()
            return JsonResponse({'message': 'Group created successfully'})
        else:
            return JsonResponse({'error': 'Group name not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def contact(request):
    return render(request, 'contact.html')


@login_required
def community(request):
    return render(request, 'community.html')

@login_required
def blog(request):
    articles = Article.objects.order_by('-date')  # Order articles by date in descending order
    return render(request, 'blog.html', {'articles': articles})

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

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

def dir(request):
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
            form.save()
            if Profile.objects.filter(user=request.user).exists():
                return render(request, 'profile.html', {'form': form, 'role_picked': True})
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            if profile.role == 'therapist':
                return redirect('view_all_therapists')
            else:  # profile.role == 'member'
                return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})

def view_all_therapists(request):
    therapists = Profile.objects.filter(role='therapist')
    return render(request, 'dir.html', {'therapists': therapists})

from django.shortcuts import get_object_or_404

def forums(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile')
    return render(request, 'forums.html', {'role': profile.role})

class CreateGroupView(View):
    def post(self, request, *args, **kwargs):
        group_name = request.POST.get('name')
        new_group = Group(name=group_name, creator=request.user)
        new_group.save()
        return JsonResponse({'message': 'Group created successfully'}, status=200)

class GetGroupsView(View):
    def get(self, request, *args, **kwargs):
        groups = Group.objects.values('name')
        return JsonResponse({'groups': list(groups)}, safe=False)

def testimonies(request):
    if request.method == 'POST':
        form = TestimoniesForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            return redirect('testimonies')
    else:
        form = TestimoniesForm()

    testimonials = Testimonies.objects.all()
    return render(request, 'testimonies.html', {'form': form, 'testimonials': testimonials})

def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonies, id=testimonial_id)
    if request.user == testimonial.user:
        testimonial.delete()
    return redirect('testimonies')

def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    article.delete()
    return redirect('blog')

@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if group_name:
            group = Group.objects.create(name=group_name)
            return JsonResponse({'success': True, 'group_name': group.name})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def fetch_group_messages(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                messages = group.messages.values('message', 'username', 'timestamp')
                return JsonResponse({'success': True, 'messages': list(messages)})
            except Group.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Group not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def book_appointment(request, therapist_id):
    # Get the therapist
    therapist = Therapist.objects.get(id=therapist_id)

    # Create a new appointment
    appointment = Appointment(therapist=therapist, date=request.POST['date'])
    appointment.save()

    # Redirect to the therapist's profile page
    return redirect('therapist_profile', therapist_id=therapist.id)

def therapist_profile(request, therapist_id):
    # Get the therapist
    therapist = Therapist.objects.get(id=therapist_id)

    # Get the appointments for this therapist
    appointments = Appointment.objects.filter(therapist=therapist)

    # Render the profile page
    return render(request, 'therapist_profile.html', {'therapist': therapist, 'appointments': appointments})
