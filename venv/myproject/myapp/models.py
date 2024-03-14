from django.db import models
from django.contrib.auth.models import User




class UserRole(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class Patient(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.firstname

class Writer(models.Model):
    name = models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u'%s' % (self.name)

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='article_images/', blank=True)

    def __str__(self):
        return self.title

