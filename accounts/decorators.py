from functools import wraps
from django.shortcuts import redirect


def approved_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_approved:
            return redirect('accounts:pending')
        return view_func(request, *args, **kwargs)
    return wrapper