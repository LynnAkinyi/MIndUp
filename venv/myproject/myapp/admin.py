from django.contrib import admin
from .models import UserRole, Writer, Article, MindfulnessTask, ExerciseTask, Task, Profile, Group, Therapist, Testimonies

# Register your models here.

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'permissions')

@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('name', 'createdDate')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_new')

@admin.register(MindfulnessTask)
class MindfulnessTaskAdmin(admin.ModelAdmin):
    list_display = ('duration', 'completed')

@admin.register(ExerciseTask)
class ExerciseTaskAdmin(admin.ModelAdmin):
    list_display = ('duration', 'completed')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('detail', 'status', 'category', 'creation_date')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'role')



@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')

@admin.register(Testimonies)
class TestimoniesAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'video', 'created_at')
