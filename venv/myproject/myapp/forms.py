from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Profile
from .models import Testimonies


class TestimoniesForm(forms.ModelForm):
    class Meta:
        model = Testimonies
        fields = ['text', 'video']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
class SignupForm(UserCreationForm):
    content = forms.CharField(widget=forms.Textarea, max_length=10000)
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
    email = forms.EmailField(widget=forms.EmailInput())
    image = forms.ImageField()
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    specialty = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Profile
        fields = ['name', 'email', 'image', 'role', 'specialty']
