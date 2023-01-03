from django.urls import path
from django.urls import reverse_lazy
from .views import (
    HomePageView,
    SignUpView,
    activate
)
from .custom_views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
)

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),

    path('signup/', SignUpView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # django.contrib.auth views
    path('login/', CustomLoginView.as_view(
        template_name = 'accounts/login.html',
    ), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_change/', CustomPasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url = reverse_lazy('home')
    ), name='password_change'),
    path('password_reset/', CustomPasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        success_url = reverse_lazy('home')
    ) , name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url = reverse_lazy('home'),
    ), name='password_reset_confirm'),
]