from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
import datetime
from django.utils import timezone
from datetime import datetime

class UserRole(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.JSONField(default=dict)

    def __str__(self):
        return self.name

class Writer(models.Model):
    name = models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u'%s' % (self.name)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    date = models.DateField(default=timezone.now)
    is_new = models.BooleanField(default=True)
class MindfulnessTask(models.Model):
    duration = models.PositiveIntegerField(default=10)  # in minutes
    completed = models.BooleanField(default=False)

class ExerciseTask(models.Model):
    duration = models.PositiveIntegerField(default=30)  # in minutes
    completed = models.BooleanField(default=False)

class Task(models.Model):
    COMPLETE = "Complete"
    INCOMPLETE = "Incomplete"
    STATUS = [
        (COMPLETE, "Complete"),
        (INCOMPLETE, "Incomplete")
    ]

    detail = models.CharField(max_length=200, default='Default detail')
    status = models.CharField(max_length=200, choices=STATUS, default=INCOMPLETE)
    category = models.CharField(max_length=200, default=None)
    creation_date = models.DateTimeField('Creation Date', default=now)
    
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

class Testimonies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    video = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Appointment(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Appointment at {self.date} with {self.therapist.name}'

class Group(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User, related_name='groups_members') 

class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
