from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
import datetime
from django.utils import timezone


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
    image = models.ImageField(upload_to='profile_images/', blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
