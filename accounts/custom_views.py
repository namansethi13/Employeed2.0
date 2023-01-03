from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .custom_decorators import logout_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)

class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "You were successfully logged in."
    redirect_authenticated_user = True
    redirect_field_name = reverse_lazy('home')
    
class CustomLogoutView(LoginRequiredMixin, SuccessMessageMixin, LogoutView):
    login_url = reverse_lazy('login')
    redirect_field_name = reverse_lazy('home')
    success_message = "You were successfully logged out."

class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    login_url = reverse_lazy('login')
    redirect_field_name = reverse_lazy('home')
    success_message = "Password Changed Successfully."

@method_decorator(logout_required, name='dispatch')
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    success_message = "Check your email inbox for password reset link."

class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    success_message = "Password Reseted Successfully."
    

