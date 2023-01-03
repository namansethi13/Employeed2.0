from django.urls import path
from .views import (
    CollegeDashboardView,
    download_sample_csv,
    upload_student_data,
    delete_course_from_college,
    retrieve_students,
)

urlpatterns = [
    path('dashboard/', CollegeDashboardView.as_view(), name='college_dashboard'),
    path('download/sample_csv/', download_sample_csv, name='download_sample_csv'),
    path('upload/students_data/', upload_student_data, name='upload_student_data'),
    path('delete/course/<int:pk>/', delete_course_from_college, name="delete_course_from_college"),
    path('students/list/<int:pk>/', retrieve_students, name ='retrieve_students'),
]