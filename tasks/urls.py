from django.urls import path

from .views import (
    AddTaskView,
    DeleteTaskView,
    HomePageView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectTasksView,
    ProjectUpdateView,
    UpdateTaskView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("projects/new/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path(
        "project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"
    ),
    path("project/<int:pk>/tasks/", ProjectTasksView.as_view(), name="project_tasks"),
    path("project/<int:pk>/add_task/", AddTaskView.as_view(), name="add_task"),
    path("project/<int:pk>/tasks/", ProjectTasksView.as_view(), name="project_tasks"),
    path("task/<int:pk>/delete/", DeleteTaskView.as_view(), name="delete_task"),
    path("tasks/update/<int:task_id>/", UpdateTaskView.as_view(), name="update_task"),
    path("tasks/delete/<int:task_id>/", DeleteTaskView.as_view(), name="delete_task"),
]
