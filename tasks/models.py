from datetime import date
from django.db import models

class Project(models.Model):
    """
    Model representing a project.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    client = models.CharField(max_length=100)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def delete(self):
        """
        Soft delete the project by setting the is_deleted flag to True.
        """
        self.is_deleted = True
        self.save()

    def __str__(self):
        """
        Return a string representation of the project.
        """
        return self.name

class Task(models.Model):
    """
    Model representing a task associated with a project.
    """
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("WIP", "Work In Progress"),
        ("ONHOLD", "On Hold"),
        ("DONE", "Done"),
    ]

    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="TODO")

    def __str__(self):
        """
        Return a string representation of the task.
        """
        return self.name
