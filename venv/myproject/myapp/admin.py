from django.contrib import admin
from .models import UserRole,  Article,  Profile,Therapist, Testimonies

# Register your models here.

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'permissions')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_new')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'role')



@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')

@admin.register(Testimonies)
class TestimoniesAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'video', 'created_at')
