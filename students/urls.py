from django.urls import path
from .views import(
    student_dashboard,
    test_register,
    JobRegistrationDetialView,
)

urlpatterns = [
    path('dashboard/',student_dashboard, name='student_dashboard'),
    path('jobs/detail/<int:pk>/', JobRegistrationDetialView.as_view(), name='job_registration_detail'),
    path('register/<int:pk>/', test_register, name='register'),
]