from django.contrib import admin

from .models import Project, Task

# Registering Project and Task models in the Django admin site
# This allows us to manage these models through the Django admin interface

admin.site.register(Project)
admin.site.register(Task)
