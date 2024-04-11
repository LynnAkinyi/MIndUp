from django.contrib import admin
from .models import (
    UserRole, Article, 
    Profile, Therapist, Testimonies, Appointment, 
    Volunteer, ChatGroup, Message, TaskProgress
)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    pass

@admin.register(Testimonies)
class TestimoniesAdmin(admin.ModelAdmin):
    pass

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    pass

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    pass
