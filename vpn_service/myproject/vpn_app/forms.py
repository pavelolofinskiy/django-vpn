from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserChangeForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile
        fields = ['first_name', 'last_name']