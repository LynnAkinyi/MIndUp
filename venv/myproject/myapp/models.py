from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
import datetime
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model

class UserRole(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.JSONField(default=dict)

    def __str__(self):
        return self.name



class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    date = models.DateTimeField(default=timezone.now)
    is_new = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    
class Profile(models.Model):
    ROLE_CHOICES = [
        ('therapist', 'Therapist'),
        ('member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    specialty = models.CharField(max_length=200, null=True, blank=True)



class Therapist(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='therapists/')
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=200, choices=Profile.ROLE_CHOICES, default='therapist')
    specialty = models.CharField(max_length=200, null=True, blank=True)
    is_new = models.BooleanField(default=True)

class Testimonies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_new = models.BooleanField(default=True)

class Appointment(models.Model):
    therapist = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # New field
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        username = 'Unknown user' if self.user is None else self.user.username
        return f'Appointment at {self.date} with {self.therapist.name} scheduled by {username}'


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class ChatGroup(models.Model):
    title = models.CharField(max_length=200, null=True)  # Ensure this is not null
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='chat_groups')

    def __str__(self):
        return self.title if self.title else 'Untitled'  # Return the title of the ChatGroup

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def username(self):
        return self.user.username

    @property
    def time(self):
        return self.timestamp.strftime('%H:%M')  # Return the time as a string in 'HH:MM' format # or '%H:%M' for 24-hour format without seconds

class OneOnOneChat(models.Model):
    members = models.ManyToManyField(get_user_model(), related_name='one_on_one_chats')

class TaskProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task1 = models.IntegerField(default=0)
    task2 = models.IntegerField(default=0)
    bonus1 = models.BooleanField(default=False)
    bonus2 = models.BooleanField(default=False)
