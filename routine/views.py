from django.shortcuts import render
from accounts.decorators import redirect_authenticated_user
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.db.models import Count

from routine import forms, models

@redirect_authenticated_user
@require_GET
def home_page(request):
    return render(request, "home.html")

@login_required
@require_GET
def dashboard_page(request):
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
@require_GET
def routine_page(request, routine_id):
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

@login_required
@require_GET
def schedule_page(request, routine_id, day):
    if day not in dict(models.Class.day_choices).values():
        raise Http404

    try:
        routine = models.Routine.objects.get(id=routine_id, user=request.user)
        day_int_value = list(filter(lambda x: x[1] == day, models.Class.day_choices))[0][0]
        classes = routine.class_set.filter(day=day_int_value)
        context = {
            "routine": routine,
            "day": day,
            "classes": classes
        }
        return render(request, "edit-schedule.html", context)
    except models.Routine.DoesNotExist:
        raise Http404

@login_required
@require_POST
def create_schedule(request, routine_id, day):
    if day not in dict(models.Class.day_choices).values():
        raise Http404

    try:
        routine = models.Routine.objects.get(id=routine_id, user=request.user)
        day_int_value = list(filter(lambda x: x[1] == day, models.Class.day_choices))[0][0]
        form = forms.ScheduleForm(request.POST)
        context = {
            "routine": routine,
            "day": day,
        }

        if form.is_valid():
            models.Class.objects.create(routine=routine, day=day_int_value,
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
                subject=form.cleaned_data["subject"],
                teacher_short_name=form.cleaned_data["teacher_short_name"])
            
            context.update({
                "classes": routine.class_set.filter(day=day_int_value),
            })
            response = render(request, "partials/schedules-with-form.html", context)
            response["HX-Trigger"] = "close-modal"

            return response

        context["scheduleForm"] = form
        return render(request, "forms/add-schedule-form.html", context)

    except models.Routine.DoesNotExist:
        raise Http404

@login_required
@require_http_methods(["DELETE"])
def delete_schedule(request, class_id):
    try:
        class_obj = models.Class.objects.get(id=class_id, routine__user=request.user)
        routine_id = class_obj.routine_id
        day = class_obj.day
        class_obj.delete()

        classes = models.Class.objects.filter(routine_id=routine_id, day=day)
        context = {
            "classes": classes,
            "oob": True
        }

        return render(request, "partials/schedules.html", context)
    except models.Class.DoesNotExist:
        raise Http404

@login_required
@require_http_methods(["GET", "POST"])
def edit_schedule(request, class_id):
    try:
        class_obj = models.Class.objects.get(id=class_id, routine__user=request.user)
        routine = class_obj.routine

        if request.method == "GET":
            form = forms.ScheduleForm({
                "start_time": class_obj.start_time,
                "end_time": class_obj.end_time,
                "subject": class_obj.subject,
                "teacher_short_name": class_obj.teacher_short_name,
            })
            context = {
                "scheduleForm": form,
                "routine": routine,
                "class": class_obj
            }
            return render(request, "forms/edit-schedule-form.html", context)
        else:
            form = forms.ScheduleForm(request.POST)

            if form.is_valid():
                class_obj.start_time = form.cleaned_data["start_time"]
                class_obj.end_time = form.cleaned_data["end_time"]
                class_obj.subject = form.cleaned_data["subject"]
                class_obj.teacher_short_name = form.cleaned_data["teacher_short_name"]
                class_obj.save()

                classes = models.Class.objects\
                    .filter(routine_id=class_obj.routine_id, day=class_obj.day)

                context = {
                    "classes": classes,
                    "oob": True
                }

                response = render(request, "partials/schedules.html", context)
                response["HX-Trigger"] = "close-modal"
                response["HX-Reswap"] = "none"
                return response
            else:
                context = {
                "scheduleForm": form,
                "routine": routine,
                "class": class_obj
                }
                return render(request, "forms/edit-schedule-form.html", context)

    except models.Class.DoesNotExist:
        raise Http404