from .views import *
from django.urls import path

urlpatterns = [
    path('', LoginViev.as_view()),
    path("registration/", RegistrationViev.as_view(), name = "registration"),
    path("Main/", BaseViev.as_view(), name = "Main"),
    path("create_project/", create_project, name = "create_project"),
    path("project_tasks/<int:pk>/", ProjectTaskViev.as_view(), name = "project_tasks"),
    path("create_project/<int:pk>/create_task/", AddTaskViev.as_view(), name = "create_task"),
    path("task_detail/<int:pk>/", TaskDetailViev.as_view(), name = "task_detail"),
    path("task_detail/<int:pk>/update/", TaskUpdateViev.as_view(), name = "task_update"),

]