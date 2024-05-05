from django.shortcuts import render
from accounts.decorators import redirect_authenticated_user
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from routine import forms, models

@redirect_authenticated_user
def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    routines = request.user.routine_set.all()
    return render(request, "dashboard.html", {"routines": routines})

@login_required
@require_POST
def create_routine(request):
    form = forms.RoutineForm(request.POST)

    if form.is_valid():
        name = form.cleaned_data["name"]
        models.Routine.objects.create(name=name, user=request.user)
        routines = request.user.routine_set.all()
        response = render(request, "partials/routines-with-form.html", {"routines": routines})
        response["HX-Trigger"] = "closeRoutineFormModal"
        return response

    return render(request, "forms/routine-form.html", {"routineForm": form})
