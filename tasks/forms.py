from django import forms

from .models import Project, Task


class ProjectForm(forms.ModelForm):
    """
    Form for creating and updating Project instances.
    """

    class Meta:
        model = Project
        fields = ["name", "description", "client", "start_date", "end_date"]


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task instances.
    """

    class Meta:
        model = Task
        fields = ["name", "description", "project", "status"]
