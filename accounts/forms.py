from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from accounts.models import User
from django import forms
from django.contrib.auth import authenticate

class UserCreationForm(BaseUserCreationForm):
    class Meta():
        model = User
        fields = ["email",]

class UserChangeForm(BaseUserChangeForm):
    class Meta():
        model = User
        fields = "__all__"
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
