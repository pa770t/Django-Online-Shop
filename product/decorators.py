from django.shortcuts import redirect

def authenticated_user(view_fun):
    def wrapper(request):
        if not request.user.is_authenticated:
            return view_fun(request)
        else:
            return redirect('home')

    return wrapper

def manager_only(view_fun):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Manager'):
            return view_fun(request, *args, **kwargs)
        else:
            return redirect('home')

    return wrapper

def customer_only(view_fun):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Customer'):
            return view_fun(request, *args, **kwargs)
        else:
            return redirect('dashboard')

    return wrapper
    