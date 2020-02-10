from django.contrib import admin
from django.urls import path, include
from .views import EmployerTaskView, EmployeeTaskView, TaskCreateView, TaskUpdateView, TaskCompleteView


urlpatterns = [

    path('task/employer_task_view/<str:username>/', EmployerTaskView.as_view(), name='work-employertaskview'),
    path('task/employee_task_view/<str:username>/', EmployeeTaskView.as_view(), name='work-employeetaskview'),
    path('task/new', TaskCreateView.as_view(), name='work-createtask'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='work-updatetask'),
    path('task/<int:pk>/complete/', TaskCompleteView.as_view(), name='work-completetask'),

]
