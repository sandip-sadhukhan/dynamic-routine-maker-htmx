from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from accounts.models import User

class UserCreationForm(BaseUserCreationForm):
    class Meta():
        model = User
        fields = ["email",]

class UserChangeForm(BaseUserChangeForm):
    class Meta():
        model = User
        fields = "__all__"