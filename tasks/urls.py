from django.urls import path

from .views import (
    AddTaskView,
    DeleteTaskView,
    HomePageView,
    ProjectCreateView,
    ProjectDeleteAPIView,
    ProjectDeleteView,
    ProjectDetailAPIView,
    ProjectDetailView,
    ProjectListAPIView,
    ProjectListView,
    ProjectTasksAPIView,
    ProjectTasksView,
    ProjectUpdateView,
    TaskDeleteAPIView,
    TaskDetailAPIView,
    TaskListAPIView,
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
    path("api-projects/", ProjectListAPIView.as_view(), name="project-list"),
    path(
        "api-projects/<int:pk>/", ProjectDetailAPIView.as_view(), name="project-detail"
    ),
    path(
        "api-projects/<int:pk>/delete/",
        ProjectDeleteAPIView.as_view(),
        name="project-delete",
    ),
    path("api-tasks/", TaskListAPIView.as_view(), name="task-list"),
    path("api-tasks/<int:pk>/", TaskDetailAPIView.as_view(), name="task-detail"),
    path("api-tasks/<int:pk>/delete/", TaskDeleteAPIView.as_view(), name="task-delete"),
    path(
        "api-projects/<int:pk>/tasks/",
        ProjectTasksAPIView.as_view(),
        name="project-tasks",
    ),
]
