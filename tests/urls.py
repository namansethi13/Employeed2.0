from django.urls import path
from .views import (
    test_delete,
    question_delete,
    question_create, 
    launch_test, 
    active_test, 
    get_test_questions,
    handle_questionlog,
    handle_tab_switch,
    handle_submit_test,
)
from .views import( TestListView, TestCreateView, TestUpdateView, TestDetailView)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',TestListView.as_view(), name='test_list'),
    path('create/', TestCreateView.as_view(), name='test_create'),
    path('delete/<int:pk>/', test_delete, name='test_delete'),
    path('update/<int:pk>/', TestUpdateView.as_view(), name='test_update'),
    path('detail/<int:pk>/', TestDetailView.as_view(), name='test_detail'),

    path('create/question/<int:pk>/', question_create, name="question_create"),
    path('delete/question/<int:pk>/', question_delete, name='question_delete'),

    path('launch/<int:pk>/', launch_test, name='launch_test'),

    path('activelist/', active_test, name='active_test'), 
    path('questions/<int:pk>', get_test_questions, name='get_test_questions'), 

    path('questions/questionlog/', handle_questionlog, name='handle_questionlog'), 
    path('questions/warning/', handle_tab_switch, name='handle_tab_switch'), 
    path('submit/', csrf_exempt(handle_submit_test), name='handle_submit_test'),
]
