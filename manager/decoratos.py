from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied


def staff_required(view_func=None, login_url=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_staff:
                if login_url:
                    login_url_resolved = reverse(login_url)
                    return redirect(login_url_resolved)
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if view_func:
        return decorator(view_func)
    return decorator
