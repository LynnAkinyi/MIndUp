from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import ArticleForm
from .models import MindfulnessTask, ExerciseTask
from .models import Profile, Group, Volunteer
from django.views.decorators.http import require_POST
from .forms import ProfileForm, TestimoniesForm
from .models import Article,  Therapist, Testimonies, Appointment, ChatGroup, Message
import base64
import uuid
from django.core.files.base import ContentFile
from django.views import View
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta



@login_required
def tasks(request):
    mindfulness_task = MindfulnessTask.objects.get_or_create(user=request.user)[0]
    exercise_task = ExerciseTask.objects.get_or_create(user=request.user)[0]

    context = {
        'mindfulness_task': mindfulness_task,
        'exercise_task': exercise_task,
    }
    return render(request, 'tasks.html', context)


@csrf_exempt
def save_task_data(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body)

        # Get the task number and bonus from the data
        task_number = data.get('taskNumber')
        bonus = data.get('bonus')

        # TODO: Save the task number and bonus to the database

        # Return a JSON response
        return JsonResponse({'status': 'success'})

    else:
        # Return a 405 Method Not Allowed response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=405)

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

    # Retrieve the appointments for the logged-in therapist
    therapist_appointments = Appointment.objects.filter(therapist=profile)

    # Get the current date
    current_date = datetime.now().date()

    # Get the date two days from now
    two_days_from_now = current_date + timedelta(days=2)

    # Retrieve the appointments for the logged-in user that are two days or less from now
    user_appointments = Appointment.objects.filter(user=request.user,)
       # Get the date two days from now
    two_days_from_now = current_date + timedelta(days=2)

    # Retrieve the appointments for the logged-in user that are two days or less from now
    upcoming_appointments = Appointment.objects.filter(user=request.user, date__range=(current_date, two_days_from_now))

    articles = Article.objects.all().order_by('-date')     # get all articles

    # add articles and appointments to the context
    context = {
        'role': profile.role, 
        'articles': articles, 
        'therapist_appointments': therapist_appointments,
        'user_appointments': user_appointments,
        'upcoming_appointments': upcoming_appointments
    }  
    
    return render(request, 'dashboard.html', context)

def book(request, therapist_id):
    # Retrieve the therapist and their appointments from the database
    therapist = get_object_or_404(Profile, id=therapist_id, role='therapist')
    appointments = Appointment.objects.filter(therapist=therapist)

    # Render the book.html template with the therapist's details and their appointments
    return render(request, 'book.html', {'therapist': therapist, 'appointments': appointments})

@require_POST
def schedule_appointment(request, therapist_id):  # therapist_id is expected here
    # Retrieve the therapist from the database
    therapist = get_object_or_404(Profile, id=therapist_id)

    # Create a new Appointment object with the selected date and save it to the database
    date = request.POST.get('date')
    appointment = Appointment(therapist=therapist, user=request.user, date=date)
    
    appointment.save()

    # Redirect the user to the dashboard
    return redirect('dashboard')

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('dashboard')

def upcoming_appointments(request):
    current_date = datetime.now().date()
    two_days_from_now = current_date + timedelta(days=2)
    upcoming_appointments = Appointment.objects.filter(user=request.user, date__range=(current_date, two_days_from_now))
    return render(request, 'upcoming_appointments.html', {'upcoming_appointments': upcoming_appointments})

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
    
    return render(request, 'forums.html')

@csrf_exempt
@require_http_methods(["GET", "POST"])
def create_group(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data['created_by'])
        Group.objects.create(name=data['name'], created_by=user)
        return JsonResponse({'status': 'success'})
    elif request.method == "GET":
        groups = Group.objects.all()
        groups_data = list(groups.values('name', 'created_by__username'))  # Convert queryset to list of dicts
        return JsonResponse(groups_data, safe=False)
    
@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        user = request.user
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)
        text = request.POST.get('message')
        Message.objects.create(user=user, group=group, text=text)
        return JsonResponse({'status': 'ok'})

@csrf_exempt
@login_required
def get_messages(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)
        messages = group.message_set.all().values('user__username', 'text', 'timestamp')
        return JsonResponse(list(messages), safe=False)    

@csrf_exempt
@require_http_methods(["GET", "POST"])
def create_volunteer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data['user'])
        try:
            Volunteer.objects.get(user=user)
            return JsonResponse({'status': 'failure', 'message': 'User is already a volunteer'})
        except ObjectDoesNotExist:
            Volunteer.objects.create(user=user)
            return JsonResponse({'status': 'success'})
    elif request.method == "GET":
        volunteers = Volunteer.objects.all()
        volunteers_data = list(volunteers.values('user__username'))  # Convert queryset to list of dicts
        return JsonResponse(volunteers_data, safe=False)
    
@csrf_exempt
def join_chat_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('group_id')
        group = ChatGroup.objects.get(id=group_id)
        group.members.add(request.user) # Add the user to the group
        group.save()
        return JsonResponse({'members': list(group.members.values_list('username', flat=True))}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_group_members(request, group_name):
    group = Group.objects.get(name=group_name)
    members = list(group.members.values('username'))
    return JsonResponse(members, safe=False)

def get_all_groups_and_members(request):
    groups = Group.objects.all()
    groups_and_members = []
    for group in groups:
        members = list(group.members.values('username'))
        groups_and_members.append({'group': group.name, 'members': members})
    return JsonResponse(groups_and_members, safe=False)

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

# def schedule_appointment(request):
#     if request.method == 'POST':
#         selected_date = request.POST.get('appointment_date')
#         if selected_date:
#             # Perform any necessary operations, such as saving to the database
#             # Here, we'll just redirect to the dashboard with the selected date
#             return redirect('dashboard', appointment_date=selected_date)
#     return redirect('book')

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
    
    
@login_required
def profile(request):
    therapists = Profile.objects.filter(role='therapist')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            if profile.role == 'therapist':
                return redirect('view_all_therapists')
            else:  # profile.role == 'member'
                return redirect('dashboard')
    else:
        try:
            profile_instance = request.user.profile
            form = ProfileForm(instance=profile_instance)
        except Profile.DoesNotExist:
            form = ProfileForm()
    return render(request, 'profile.html', {'form': form, 'therapists': therapists})

def therapist_detail(request, therapist_id):
    try:
        therapist = Profile.objects.get(id=therapist_id, role='therapist')
    except Profile.DoesNotExist:
        raise Http404("Therapist does not exist")
    return render(request, 'therapist_detail.html', {'therapist': therapist})



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


# def book_appointment(request, therapist_id):
#     # Get the therapist
#     therapist = get_object_or_404(Profile, id=therapist_id, role='therapist')

#     # Create a new appointment
#     appointment = Appointment(therapist=therapist, date=request.POST['date'])
#     appointment.save()

#     # Redirect to the therapist's profile page
#     return redirect('therapist_profile', therapist_id=therapist.id)


# def therapist_profile(request, therapist_id):
#     # Get the therapist
#     therapist = get_object_or_404(Profile, id=therapist_id, role='therapist')

#     # Get the appointments for this therapist
#     appointments = Appointment.objects.filter(therapist=therapist)

#     # Render the profile page
#     return render(request, 'therapist_profile.html', {'therapist': therapist, 'appointments': appointments})


@csrf_exempt
def create_chat_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the JSON data
        title = data.get('title')  # Get the 'title' from the parsed data
        if title is not None and title.strip():  # Check if 'title' is not empty
            chat_group = ChatGroup.objects.create(title=title, created_by=request.user)
            return JsonResponse({'title': chat_group.title}, status=201)
        else:
            return JsonResponse({'error': 'Title cannot be empty'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_chat_groups(request):
    if request.method == 'GET':
        groups = ChatGroup.objects.all()
        return JsonResponse([{
            'id': group.id,
            'title': group.title,
            'members': list(group.members.values_list('username', flat=True)), # Include the list of members
        } for group in groups], safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
