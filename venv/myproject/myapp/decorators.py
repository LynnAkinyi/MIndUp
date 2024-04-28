# decorators.py

from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser

def patient_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == CustomUser.PATIENT:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapped_view
