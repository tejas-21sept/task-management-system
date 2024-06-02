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
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .forms import ProjectForm, TaskForm
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .utils import api_response


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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProjectListAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.filter(is_deleted=False).prefetch_related("task_set")
    serializer_class = ProjectSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            data=serializer.data, message="Project list retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return api_response(
            data=serializer.data,
            message="Project created successfully",
            code=status.HTTP_201_CREATED,
        )


class ProjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.filter(is_deleted=False).prefetch_related("task_set")
    serializer_class = ProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(
            data=serializer.data, message="Project details retrieved successfully"
        )


class ProjectDeleteAPIView(generics.DestroyAPIView):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return api_response(
            data=None,
            message="Project deleted successfully",
            code=status.HTTP_204_NO_CONTENT,
        )


class TaskListAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.select_related("project").filter(project__is_deleted=False)
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            data=serializer.data, message="Task list retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return api_response(
            data=serializer.data,
            message="Task created successfully",
            code=status.HTTP_201_CREATED,
        )


class TaskDetailAPIView(generics.RetrieveAPIView):
    queryset = Task.objects.select_related("project")
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(
            data=serializer.data, message="Task details retrieved successfully"
        )


class TaskDeleteAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_destroy(self, instance):
        instance.delete()
        return api_response(
            data=None,
            message="Task deleted successfully",
            code=status.HTTP_204_NO_CONTENT,
        )


class ProjectTasksAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.kwargs["pk"]
        return Task.objects.filter(project_id=project_id).select_related("project")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            data=serializer.data, message="Project tasks retrieved successfully"
        )
