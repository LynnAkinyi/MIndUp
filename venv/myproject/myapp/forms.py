from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article

class ArticleForm(forms.ModelForm):  # Use ModelForm instead of Form
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


