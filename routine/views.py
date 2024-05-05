from django.shortcuts import render
from accounts.decorators import redirect_authenticated_user
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Count

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

@login_required
@require_http_methods(["DELETE"])
def delete_routine(request, routine_id):
    try:
        routine = models.Routine.objects.get(id=routine_id, user=request.user)
        routine.delete()
        routines = request.user.routine_set.all()
        context = {"routines": routines, "oob": True}
        return render(request, "partials/routines.html", context)
    except models.Routine.DoesNotExist:
        raise Http404

@login_required
def edit_routine(request, routine_id):
    try:
        routine = models.Routine.objects.get(id=routine_id, user=request.user)

        # No of classes data
        classes_count_data = {}
        for day in list(dict(models.Class.day_choices).values()):
            classes_count_data[day] = 0

        qs_data = list(routine.class_set.all().values("day")
                    .annotate(class_count=Count("day")))

        for d in qs_data:
            day = dict(models.Class.day_choices).get(d["day"])
            classes_count_data[day] = d["class_count"]
        
        context =  {
            "routine": routine,
            "classes_count_data": classes_count_data
        }

        return render(request, "edit-routine.html", context)
    except models.Routine.DoesNotExist:
        raise Http404
