from datetime import date

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProjectForm, TaskForm
from .models import Project, Task

class ProjectDeleteView(View):
    """
    View to handle the deletion of a project.
    """
    def post(self, request, pk):
        """
        Handles the POST request to delete a project by its primary key.
        """
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return JsonResponse({"success": True})

class HomePageView(ListView):
    """
    View to display the home page with a list of ongoing projects.
    """
    template_name = "tasks/homepage.html"
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        """
        Returns a queryset of projects that have not ended.
        """
        return Project.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gt=timezone.now()), is_deleted=False
        )

class ProjectListView(ListView):
    """
    View to display a list of projects.
    """
    model = Project
    template_name = "tasks/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        """
        Returns a queryset of projects that have not ended.
        """
        return Project.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gt=timezone.now()), is_deleted=False
        )

class ProjectCreateView(CreateView):
    """
    View to handle the creation of a new project.
    """
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"
    success_url = reverse_lazy("homepage")

class ProjectDetailView(DetailView):
    """
    View to display the details of a specific project.
    """
    model = Project
    template_name = "tasks/project_detail.html"

    def get_context_data(self, **kwargs):
        """
        Adds the list of tasks associated with the project to the context.
        """
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.task_set.all()
        return context

class ProjectUpdateView(UpdateView):
    """
    View to handle the update of an existing project.
    """
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"
    success_url = reverse_lazy("homepage")

class ProjectTasksView(ListView):
    """
    View to display the tasks associated with a specific project.
    """
    template_name = "tasks/project_tasks.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        """
        Adds the project and its tasks to the context.
        """
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("pk")
        context["project"] = get_object_or_404(Project, pk=project_id)
        return context

    def get_queryset(self):
        """
        Returns a queryset of tasks for the specified project.
        """
        project_id = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=project_id)
        return Task.objects.filter(project=project)

class UpdateTaskView(View):
    """
    View to handle the update of an existing task.
    """
    def post(self, request, task_id):
        """
        Handles the POST request to update a task by its ID.
        """
        task = get_object_or_404(Task, id=task_id)
        name = request.POST.get("name")
        description = request.POST.get("description")
        status = request.POST.get("status")

        # Update task attributes
        task.name = name or task.name
        task.description = description or task.description
        task.status = status or task.status
        task.save()
        return JsonResponse({"success": True})

class DeleteTaskView(View):
    """
    View to handle the deletion of an existing task.
    """
    def post(self, request, task_id):
        """
        Handles the POST request to delete a task by its ID.
        """
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({"success": True})

class AddTaskView(CreateView):
    """
    View to handle the creation of a new task.
    """
    model = Task
    fields = ["name", "description", "status"]

    def form_valid(self, form):
        """
        Assigns the task to the specified project before saving the form.
        """
        form.instance.project_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects to the project tasks view after successfully adding a task.
        """
        project_id = self.kwargs["pk"]
        return reverse_lazy("project_tasks", kwargs={"pk": project_id})
