from django.shortcuts import redirect

def redirect_authenticated_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return view(request, *args, **kwargs)
    return wrapper