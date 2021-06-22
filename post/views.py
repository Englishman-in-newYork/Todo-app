from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from .models import User, Project, Tasks
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import *


class BaseViev(View):
    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        context = {"projects": projects}
        return render(request, "Projects.html", context)


class ProjectTaskViev(View):
    TASK_STATUSES = {
        "TASK_STATUS_WAITING": "Waiting",
        "TASK_STATUS_IMPLEMENTATION": "Implementation",
        "TASK_STATUS_VERIFYING": "Verifying",
        "TASK_STATUS_RELEASING": "Releasing"}

    def get(self, request, pk, *args, **kwargs):
        search_query = request.GET.get("search", "")
        statuses = self.TASK_STATUSES.values
        filter_query = request.GET.get("filter")
        project_key = Project.objects.filter(id=pk)
        projects = Project.objects.get(id=pk)


        if filter_query:
            filter = tasks = Tasks.objects.filter(project = projects, status_task__icontains=filter_query)
            context = {"tasks": tasks,
                       "projects": projects,
                       "project_key": project_key,
                       "filter": filter,
                       "statuses": statuses
                       }
            return render(request, "Project_tasks.html", context)

        elif search_query:
            search = tasks = Tasks.objects.filter(project=projects,title__icontains=search_query)
            context = {"tasks": tasks,
                       "projects": projects,
                       "project_key": project_key,
                       "search":search,
                       "statuses":statuses
                       }
            return render(request,"Project_tasks.html", context)

        else:
            tasks = Tasks.objects.filter(project=projects)
            context = {"tasks": tasks,
                    "projects": projects,
                    "project_key":project_key,
                    "statuses":statuses
                    }
            return render(request, "Project_tasks.html", context)



class TaskDetailViev(View):

    def get(self, request, pk, *args, **kwargs):
        tasks = Tasks.objects.filter(id=pk)
        context = {"tasks":tasks}
        return render(request, "Task_detail.html", context)


class TaskUpdateViev(UpdateView):
    model = Tasks
    template_name = "Update_task.html"
    form_class = UpdateTaskForm


class LoginViev(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {"form": form}
        return render(request, "Loggin.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("Main")  # Редирект на главную страницу
        context = {"form": form}
        return render(request, "Loggin.html", context)


class RegistrationViev(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {"form": form}
        return render(request, "Register.html", context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data["username"]
            new_user.email = form.cleaned_data["email"]
            new_user.save()
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            login(request, user)
            return HttpResponseRedirect("/")
        context = {"form": form}
        return render(request, "Register.html", context)


def create_project(request):
    error = ''
    if request.method == "POST":
        form = AddNewProjectForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.save()
            return redirect("Main")
        else:
            error = "Incorrect form filling"

    form = AddNewProjectForm()
    data = {
        "form": form,
        "error": error
    }
    return render(request, "Create_project.html", data)


# def create_task(request, pk):
#     error = ''
#     if request.method == "POST":
#         form = AddNewTaskForm(request.POST)
#         if form.is_valid():
#             response = form.save(commit=False)
#             response.user = request.user
#             response.save()
#             return redirect("project_tasks")
#         else:
#             error = "Incorrect form filling"
#
#     form = AddNewTaskForm()
#     projects = Project.objects.get(id=pk)
#     tasks = Tasks.objects.filter(project=projects)
#     data = {
#         "form": form,
#         "error": error,
#         "tasks": tasks,
#         "projects": projects
#     }
#     return render(request, "Create_task.html", data)

class AddTaskViev(View):
    def get(self, request,pk, *args, **kwargs):
        form = AddNewTaskForm(request.POST or None, initial={"project":pk})
        form.project = pk
        context = {"form":form,}
        return render(request, "Create_task.html", context)

    def post(self,request, pk, *args, **kwargs):
        form = AddNewTaskForm(request.POST or None, initial={"project":Project.objects.get(id=pk)})
        if form.is_valid():
            responce = form.save(commit=False)
            responce.user = request.user
            responce.save()
            return redirect("Main")
        else:
            error = "Incorrect form filling"
        context = {"form": form,
                   "error":error}
        return render(request, "Create_task.html", context)

