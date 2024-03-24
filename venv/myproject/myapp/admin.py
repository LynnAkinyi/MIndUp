from django.contrib import admin
from .models import Article, Profile, Writer, MindfulnessTask, ExerciseTask, Task, UserRole


# Register your models here.



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'role']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'permissions']

@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ['name', 'createdDate']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'image', 'date']

@admin.register(MindfulnessTask)
class MindfulnessTaskAdmin(admin.ModelAdmin):
    list_display = ['duration', 'completed']

@admin.register(ExerciseTask)
class ExerciseTaskAdmin(admin.ModelAdmin):
    list_display = ['duration', 'completed']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['detail', 'status', 'category', 'creation_date']


