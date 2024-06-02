from django.urls import path

from .views import (  # TaskCreateView,; TaskDeleteView,; TaskListView,; TaskUpdateView,
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
    DeleteTaskView
)

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("projects/new/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path(
        "project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"
    ),
    # path("tasks/", TaskListView.as_view(), name="task_list"),
    # path("tasks/new/", TaskCreateView.as_view(), name="task_create"),
    # path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    # path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("project/<int:pk>/tasks/", ProjectTasksView.as_view(), name="project_tasks"),
    path("project/<int:pk>/add_task/", AddTaskView.as_view(), name="add_task"),
    path("project/<int:pk>/tasks/", ProjectTasksView.as_view(), name="project_tasks"),
    path("task/<int:pk>/delete/", DeleteTaskView.as_view(), name="delete_task"),
    path("tasks/update/<int:task_id>/", UpdateTaskView.as_view(), name="update_task"),
    path("tasks/delete/<int:task_id>/", DeleteTaskView.as_view(), name="delete_task"),
]
