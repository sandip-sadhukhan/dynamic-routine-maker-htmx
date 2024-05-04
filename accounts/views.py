from django.shortcuts import render
from django.contrib.auth import authenticate, login as authLogin
from accounts.forms import LoginForm
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST
from accounts.decorators import redirect_authenticated_user
from django.urls import reverse


@require_POST
@redirect_authenticated_user
def login(request):
    form = LoginForm(request.POST)

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
