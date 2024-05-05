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


class SignupForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email already exists")

        return email
    
    def clean_password(self):
        password = self.cleaned_data["password"]

        if len(password) < 8:
            self.add_error("password", "Password must be at least 8 characters long")

        return password
    