from django.contrib import admin
from .models import Article, Profile


# Register your models here.



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'role']
