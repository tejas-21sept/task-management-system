from datetime import date

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    client = models.CharField(max_length=100)
    # start_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("WIP", "Work In Progress"),
        ("ONHOLD", "On Hold"),
        ("DONE", "Done"),
    ]

    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="TODO")

    def __str__(self):
        return self.name
