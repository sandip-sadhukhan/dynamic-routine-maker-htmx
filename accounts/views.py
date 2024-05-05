from django.shortcuts import render
from django.contrib.auth import authenticate, login as authLogin, logout as authLogout
from accounts import forms
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST
from accounts.decorators import redirect_authenticated_user
from django.urls import reverse
from accounts.models import User
from django.shortcuts import redirect


@require_POST
@redirect_authenticated_user
def login(request):
    form = forms.LoginForm(request.POST)

    if not form.is_valid():
        return render(request, "forms/login-form.html", {"loginForm": form})

    email = form.cleaned_data["email"]
    password = form.cleaned_data["password"]
    user = authenticate(request, email=email, password=password)

    if user is not None:
        authLogin(request, user)
        response = HttpResponse()
        response["HX-Redirect"] = reverse("dashboard")
        return response
    else:
        form.add_error("password", "Invalid credentials")
        return render(request, "forms/login-form.html", {"loginForm": form})


@require_POST
@redirect_authenticated_user
def signup(request):
    form = forms.SignupForm(request.POST)

    if not form.is_valid():
        return render(request, "forms/signup-form.html", {"signupForm": form})
    
    email = form.cleaned_data["email"]
    password = form.cleaned_data["password"]

    user = User.objects.create_user(email=email, password=password)
    authLogin(request, user)
    response = HttpResponse()
    response["HX-Redirect"] = reverse("dashboard")
    return response

def logout(request):
    authLogout(request)
    return redirect("home")