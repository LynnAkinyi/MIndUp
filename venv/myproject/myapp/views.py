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
from .models import Profile, Volunteer
from django.views.decorators.http import require_POST
from .forms import ProfileForm, TestimoniesForm
from .models import Article,  Therapist, Testimonies, Appointment, ChatGroup, Message
import base64
import uuid
from django.core.files.base import ContentFile
from django.views import View
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.utils import timezone
from datetime import datetime, timedelta
from .models import TaskProgress, DirectMessage, DeletionReason
from django.db.models import Q
from .utils import create_google_meeting_link
from django.contrib import messages
from datetime import datetime




@csrf_exempt
def get_direct_messages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sender = data.get('sender')
        receiver = data.get('receiver')

        messages = DirectMessage.objects.filter(
            sender__username=sender, receiver__username=receiver
        ).order_by('timestamp')

        messages_list = list(messages.values('sender__username', 'receiver__username', 'message', 'timestamp'))

        return JsonResponse(messages_list, safe=False)

def get_progress(request):
    try:
        progress = TaskProgress.objects.filter(user=request.user).latest('id')
        data = {
            'task1': progress.task1,
            'task2': progress.task2,
            'bonus1': progress.bonus1,
            'bonus2': progress.bonus2,
        }
        return JsonResponse(data)
    except TaskProgress.DoesNotExist:
        return JsonResponse({})

@csrf_exempt
def update_progress(request):
    if request.method == 'POST':
        task1 = request.POST.get('task1')
        task2 = request.POST.get('task2')
        bonus1 = True if request.POST.get('bonus1') == 'on' else False
        bonus2 = True if request.POST.get('bonus2') == 'on' else False

        progress = TaskProgress(user=request.user, task1=task1, task2=task2, bonus1=bonus1, bonus2=bonus2)
        progress.save()

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "invalid request"})



def index(request):
    return render(request, 'index.html')

def tasks(request):
    return render(request, 'tasks.html')



def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile')

    # Retrieve the appointments for the logged-in therapist
    therapist_appointments = Appointment.objects.filter(therapist=profile, date__gte=timezone.now()).order_by('date')

    # Get the current date
    current_date = datetime.now().date()
   
    
    new_articles = Article.objects.filter(is_new=True)
    new_therapists = Therapist.objects.filter(is_new=True)

    # Get the date two days from now
    two_days_from_now = current_date + timedelta(days=2)

    # Retrieve the appointments for the logged-in user that are two days or less from now
    user_appointments = Appointment.objects.filter(user=request.user, date__gte=timezone.now()).order_by('date')
       # Get the date two days from now
    two_days_from_now = current_date + timedelta(days=2)

    # Retrieve the appointments for the logged-in user that are two days or less from now
    upcoming_appointments = Appointment.objects.filter(user=request.user, date__range=(current_date, two_days_from_now), date__gte=timezone.now()).order_by('date')
    
    # Get the current date and time
    now = timezone.now()
    start_of_day = now - timedelta(days=1)

    # Get the start and end of the current day
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    articles = Article.objects.filter(date__range=(start_of_day, end_of_day)).order_by('-date')     # get all articles
    new_testimonies = Testimonies.objects.filter(created_at__gte=start_of_day, is_new=True)
    
    deletion_reasons = DeletionReason.objects.filter(
    Q(user=request.user) | Q(therapist=request.user)
).order_by('-created_at')

    # add articles and appointments to the context
    context = {
        'role': profile.role, 
        'articles': articles, 
        'therapist_appointments': therapist_appointments,
        'user_appointments': user_appointments,
        'upcoming_appointments': upcoming_appointments,   
        'deletion_reasons': deletion_reasons,     
        'new_articles': new_articles,
        'testimonials': new_testimonies,
        'new_therapists': new_therapists,
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

    # Get the selected date and time
    date_str = str(request.POST.get('date'))
    time_str = str(request.POST.get('time'))

    # Combine the date and time into a single datetime object
    date_time_str = f"{date_str} {time_str}"
    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

    # Check if an appointment already exists for the user on the selected date
    existing_appointment = Appointment.objects.filter(user=request.user, date=date_time_obj).exists()
    if existing_appointment:
        messages.error(request, 'You have already scheduled an appointment on this date.')
        # Render the current page with the error message
        return render(request, 'book.html', {'therapist': therapist})

    # Create a new Appointment object and save it to the database
    appointment = Appointment(therapist=therapist, user=request.user, date=date_time_obj)
    
    # Generate the Google Meet link for the appointment
    create_google_meeting_link(appointment)
    
    appointment.save()

    # Redirect the user to the dashboard
    return redirect('dashboard')

@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        reason = request.POST.get('delete_reason')
        DeletionReason.objects.create(
            user=request.user,
            appointment_id=appointment_id,
            therapist=appointment.therapist.user,  # Use the User instance associated with the Profile
            reason=reason
        )
    
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

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.save()
            return redirect('blog')
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

def read(request ):
    articles = Article.objects.order_by('-date')  # Order articles by date in descending order
    return render(request, 'read.html', {'articles': articles})

def faq(request):
    return render(request, 'faq.html')


# def forums(request):
    
#     return render(request, 'forums.html')
    

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
    
def get_volunteers(request):
    volunteers = Volunteer.objects.all()
    volunteer_list = list(volunteers.values('user__username', 'user_id'))  # Include 'user_id' here
    return JsonResponse(volunteer_list, safe=False)

def contact(request):
    return render(request, 'contact.html')


@login_required
def community(request):
    therapists = Therapist.objects.all()[:4]
    return render(request, 'community.html', {'therapists': therapists})

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

@login_required
def dir(request, view_all=False):
    therapists = Profile.objects.filter(role='therapist')
    if not view_all:
        therapists = therapists[:6]
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
def profile(request, user_id=None):
    user_id = user_id or request.user.id
    user = User.objects.get(id=user_id)
    therapists = Profile.objects.filter(role='therapist')

    try:
        profile_instance = user.profile
    except Profile.DoesNotExist:
        profile_instance = Profile(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            if profile_instance.role == 'therapist':
                return redirect('view_all_therapists')
            else:  # profile.role == 'member'
                return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile_instance)

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
        form = TestimoniesForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            return redirect('testimonies')
    else:
        form = TestimoniesForm()

    testimonials = Testimonies.objects.order_by('-created_at')
    return render(request, 'testimonies.html', {'form': form, 'testimonials': testimonials})



def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonies, id=testimonial_id)
    if request.user == testimonial.user:
        testimonial.delete()
    return redirect('testimonies')

def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    print(f"User: {request.user}, Article Creator: {article.creator}")
    if request.user != article.creator:
        return HttpResponseForbidden()
    article.delete()
    return redirect('blog')


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

@csrf_exempt
@require_http_methods(["GET", "POST"])
def create_group(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data['created_by'])
        ChatGroup.objects.create(name=data['name'], created_by=user)
        return JsonResponse({'status': 'success'})
    elif request.method == "GET":
        groups = ChatGroup.objects.all()
        groups_data = list(groups.values('name', 'created_by__username'))  # Convert queryset to list of dicts
        return JsonResponse(groups_data, safe=False)
    
@csrf_exempt
@require_http_methods(["GET", "POST"])
def create_group(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data['created_by'])
        ChatGroup.objects.create(name=data['name'], created_by=user)
        return JsonResponse({'status': 'success'})
    elif request.method == "GET":
        groups = ChatGroup.objects.all()
        groups_data = list(groups.values('name', 'created_by__username'))  # Convert queryset to list of dicts
        return JsonResponse(groups_data, safe=False)    
    
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('group_id')
        message_text = data.get('message_text')

        try:
            # Fetch the group
            group = ChatGroup.objects.get(id=group_id)

            # Check if the user is a member of the group
            if request.user in group.members.all():
                # Create and save the message
                message = Message(user=request.user, group=group, text=message_text)
                message.save()

                return JsonResponse({'status': 'Message sent'}, status=200)
            else:
                # If the user is not a member of the group, raise a permission error
                raise PermissionDenied('You are not a member of this group')
        except ChatGroup.DoesNotExist:
            return JsonResponse({'error': 'Group not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@login_required
def get_messages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('group_id')
        try:
            group_id = int(group_id)  # Try to convert group_id to an integer
            group = ChatGroup.objects.get(id=group_id)
            messages = group.message_set.all().values('user__username', 'text', 'timestamp')
        except ValueError:
            # If group_id is not a number, treat it as a username
            receiver_username = group_id
            sender = request.user
            try:
                receiver = User.objects.get(username=receiver_username)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            messages = DirectMessage.objects.filter(sender=sender, receiver=receiver).values('sender__username', 'message', 'timestamp')
        except ChatGroup.DoesNotExist:
            return JsonResponse({'error': 'Group not found'}, status=404)
        messages = list(messages)
        for message in messages:
            message['username'] = message.pop('user__username' if 'user__username' in message else 'sender__username')
            message['time'] = message.pop('timestamp')
        return JsonResponse(messages, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
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
    group = ChatGroup.objects.get(name=group_name)
    members = list(group.members.values('username'))
    return JsonResponse(members, safe=False)

def get_all_groups_and_members(request):
    groups = ChatGroup.objects.all()
    groups_and_members = []
    for group in groups:
        members = list(group.members.values('username'))
        groups_and_members.append({'group': group.name, 'members': members})
    return JsonResponse(groups_and_members, safe=False)    
