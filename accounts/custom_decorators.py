from django.urls import reverse_lazy
from django.shortcuts import redirect

def logout_required(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        else:
            return func(request, *args, **kwargs)
    return inner