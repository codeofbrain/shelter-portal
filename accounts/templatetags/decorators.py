from django.core.exceptions import PermissionDenied
from functools import wraps

def user_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            has_role = getattr(request.user, role, False)
            if has_role or request.user.is_superuser or request.user.leiterin:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

