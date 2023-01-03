from django.urls import path
from .views import(
   notifications,
)

urlpatterns = [
    path('all/',notifications, name='notfications'),
]