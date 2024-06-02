# forms.py
from django import forms

from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "client", "start_date", "end_date"]


# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ["name", "description", "client", "end_date"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "project", "status"]
