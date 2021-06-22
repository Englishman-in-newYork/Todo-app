from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Project(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, null =True)
    title = models.CharField(max_length=255, verbose_name="Title", null=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date of create")


    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


    def __str__(self):
        return self.title


class Tasks(models.Model):

    TASK_STATUS_WAITING = "Waiting"
    TASK_STATUS_IMPLEMENTATION = "Implementation"
    TASK_STATUS_VERIFYING = "Verifying"
    TASK_STATUS_RELEASING = "Releasing"

    TASK_STATUS = (
        (TASK_STATUS_WAITING, "Waiting"),
        (TASK_STATUS_IMPLEMENTATION, "Implementation"),
        (TASK_STATUS_VERIFYING, "Verifying"),
        (TASK_STATUS_RELEASING, "Releasing")
    )

    project = models.ForeignKey(Project, verbose_name="Project", on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, verbose_name="Task title", null=False)
    description = models.TextField(verbose_name="Task description")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Datetime")
    status_task = models.CharField(max_length=50, choices=TASK_STATUS, default=TASK_STATUS_WAITING,
                                   verbose_name="Status of task")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, null=True)


    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def get_absolute_url(self):
        return f"/task_detail/{self.id}/"

    def __str__(self):
        return f"{self.title}-({self.project})"
