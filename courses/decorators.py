from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def department_head_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'instructor' and request.user.instructor.is_department_head:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Access Denied: You do not have permission to access this page.')
            return redirect('dashboard') 
    return wrapper