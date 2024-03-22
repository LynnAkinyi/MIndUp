from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Profile


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',  'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('therapist', 'Therapist'),
        ('member', 'Member'),
    ]

    name = forms.CharField(widget=forms.TextInput())
    image = forms.ImageField()
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Profile
        fields = ['name', 'image', 'role']
