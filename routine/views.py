from django.shortcuts import render
from accounts.decorators import redirect_authenticated_user
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@redirect_authenticated_user
def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    routines = request.user.routine_set.all()
    return render(request, "dashboard.html", {"routines": routines})