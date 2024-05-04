from django.shortcuts import render
from accounts.decorators import redirect_authenticated_user
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@redirect_authenticated_user
def homePage(request):
    return render(request, "index.html")

@login_required
def dashboard(request):
    return HttpResponse("hi")
    return render(request, "dashboard.html")