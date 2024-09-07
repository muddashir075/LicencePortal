from django.contrib.auth.decorators import user_passes_test
def allowed_roles(allowed_roles):
    def decorator(view_func):
        @user_passes_test(lambda user: user.role in allowed_roles)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator