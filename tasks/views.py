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
from django.views.generic.edit import UpdateView

from .forms import ProjectForm, TaskForm
from .models import Project, Task


class ProjectDeleteView(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return JsonResponse({"success": True})


class HomePageView(ListView):
    template_name = "tasks/homepage.html"
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        # Filter projects where end_date is either None or greater than the current date
        # and where is_deleted is False
        qs = Project.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gt=timezone.now()), is_deleted=False
        )

        print(f"\nQS -  {qs}\n")
        return qs
        # return Project.objects.filter(
        #     Q(end_date__isnull=True) | Q(end_date__gt=timezone.now()), is_deleted=True
        # )


class ProjectListView(ListView):
    model = Project
    template_name = "tasks/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        # Filter projects where end_date is either None or greater than the current date
        # and where is_deleted is False
        qs = Project.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gt=timezone.now()), is_deleted=True
        )

        print(f"\nQS -  {qs}\n")
        return Project.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gt=timezone.now()), is_deleted=True
        )


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"
    success_url = reverse_lazy("homepage")


class ProjectDetailView(DetailView):
    model = Project
    template_name = "tasks/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.task_set.all()
        return context

    # class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "tasks/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"
    success_url = reverse_lazy("homepage")


# class TaskListView(ListView):
#     model = Task
#     template_name = "tasks/task_list.html"
#     context_object_name = "tasks"


# class TaskCreateView(CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name = "tasks/task_form.html"
#     success_url = reverse_lazy("task_list")


# class TaskUpdateView(UpdateView):
#     model = Task
#     form_class = TaskForm
#     template_name = "tasks/task_form.html"
#     success_url = reverse_lazy("task_list")


# class TaskDeleteView(DeleteView):
# model = Task
# template_name = "tasks/task_confirm_delete.html"
# success_url = reverse_lazy("task_list")


from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, ListView

from .models import Project, Task


class ProjectTasksView(ListView):
    model = Task
    template_name = "tasks/project_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        print(f"\nInside ProjectTasksView - {self.kwargs}\n")
        project_id = self.kwargs["pk"]
        return Task.objects.filter(project_id=project_id)


from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Project, Task


class ProjectTasksView(ListView):
    template_name = "tasks/project_tasks.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        print(f"\nget_context_data - {kwargs}\n")
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("pk")
        context["project"] = get_object_or_404(Project, pk=project_id)
        return context

    def get_queryset(self):
        print(f"\nget_queryset - {self.kwargs}\n")
        project_id = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=project_id)
        qs = Task.objects.filter(project=project)
        print(f"\nQS - {qs}\n")
        return qs


# from django.urls import reverse_lazy
# from django.views.generic.edit import DeleteView

# from .models import Task


# class DeleteTaskView(DeleteView):
#     model = Task
#     template_name = "tasks/task_confirm_delete.html"

#     def get_success_url(self):
#         project_id = self.object.project.id
#         return reverse_lazy("project_tasks", kwargs={"pk": project_id})


# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404

# from .models import Task


# def update_task(request, task_id):
#     if request.method == "POST":
#         task = get_object_or_404(Task, id=task_id)
#         task.name = request.POST.get("name")
#         task.description = request.POST.get("description")
#         task.status = request.POST.get("status")
#         task.save()
#         return JsonResponse({"success": True})
#     return JsonResponse({"success": False}, status=400)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Task


class UpdateTaskView(View):
    def post(self, request, task_id):
        print(f"\nUpdateTaskView - {UpdateTaskView} ||\n")
        print(f"\ndata - {request.POST}\n")
        task = get_object_or_404(Task, id=task_id)
        print(f"\ntask1 - {task}\n")
        name = request.POST.get("name")
        description = request.POST.get("description")
        status = request.POST.get("status")
        print(f"\nstatus - {status}\n")
        print(f"\name - {name}\n")
        print(f"\description - {description}\n")

        # Update task attributes
        task.name = name if name else task.name
        task.description = description if description else task.description
        task.status = status if status else task.status
        task.save()
        print(f"\nstatus1 - {task.status}\n")
        print(f"\name1 - {task.name}\n")
        print(f"\description1 - {task.description}\n")
        print(f"\ntask2 - {task}\n")

        return JsonResponse({"success": True})


class DeleteTaskView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({"success": True})


from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Task


class AddTaskView(CreateView):
    model = Task
    fields = ["name", "description", "status"]

    def form_valid(self, form):
        print(f"\nAddTaskView Form Valid - {self.kwargs}\n")
        form.instance.project_id = self.kwargs["pk"]  # Assign the project ID
        return super().form_valid(form)

    def get_success_url(self):
        print(f"\nAddTaskView success url - {self.kwargs}\n")
        project_id = self.kwargs["pk"]
        return reverse_lazy("project_tasks", kwargs={"pk": project_id})
