from django.urls import path
from .views import (
    JobListView, 
    JobDetialView, 
    JobUpdateView,
)
from .views import (
    job_create_view,
    job_delete_view,
    job_post_background
)

urlpatterns = [
    path("jobs/list/", JobListView.as_view(), name='job_list'),
    path("jobs/create/", job_create_view, name='job_create'),
    path("jobs/detail/<int:pk>/", JobDetialView.as_view(), name='job_detail'),
    path("jobs/update/<int:pk>/", JobUpdateView.as_view(), name='job_update'),
    path("jobs/delete/<int:pk>/", job_delete_view, name="job_delete"),

    path('jobs/post/<int:pk>/', job_post_background, name='job_post'),
]