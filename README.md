# Task Management System

## Description

This repository contains a Django-based task management system. The system allows users to manage projects and tasks, including creating, viewing, editing, and deleting tasks and projects. The primary features include task status management and project-specific task lists.

## Features

### Tasks
- **List all the tasks**: View all tasks in the system.
- **Create a new task**: Add a new task to a project.
- **Delete a task**: Remove an existing task.
- **Edit the task status**: Change the status of a task (TODO, WIP, ONHOLD, DONE).

### Projects
- **List all the projects**: View all projects that have not ended.
- **Create a new project**: Add a new project.
- **Delete a project**: Remove an existing project.
- **View a project**: View details of a specific project.
- **Show list of all the tasks for that particular project**: View tasks associated with a project.

## Database Design

### Project
- **Name**: The name of the project.
- **Description**: A brief description of the project.
- **Client**: Foreign key to the client.
- **StartDate**: The day when the entry is created.
- **EndDate**: The end date of the project.

### Task
- **Name**: The name of the task.
- **Description**: A brief description of the task.
- **Project**: Foreign key to the project.
- **Status**: The current status of the task (TODO, WIP, ONHOLD, DONE).

## Setup and Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/task-management-system.git
   cd task-management-system/task_management

2. **Create a virtual environment and activate it**:
    i.Open a terminal:

      - Windows: Open `Command Prompt` or `PowerShell`.
      - macOS/Linux: Open a terminal window.

    
    ii. Navigate to the project directory:

      ```python
        cd social_network_backend
    
      ```


    iii. Create the virtual environment:

      ```python
        python -m venv venv

      ```

    iv. Activate the virtual environment:


      ```python

        source venv/bin/activate  # Linux/macOS

        venv\Scripts\activate.bat  # Windows 

      ```


3. **Install dependencies**:

  ```pip
    pip install -r requirements.txt
  ``` 

4. **Run the migrations**:
    ```python
        python manage.py makemigrations
        python manage.py migrate
    ``` 

5. **Start the development server**:
    ```python
        python manage.py runserver
    ``` 
