# Task Manager / Kanban Board

A Django web application for managing tasks. Allows users to create, update, and delete tasks through an admin panel and a REST API.

## Features
- User authentication
- Task creation, update, delete
- Creating teams
- API support using Django Rest Framework

## Installation
1. Clone front end and back end repositories
- git clone git@github.com:MartinInglin/todo-list-backend.git
- git clone git@github.com:MartinInglin/todo-list-frontend.git

2. Navigate in the the project
- cd project_name

3. Set up a virtual environment
- python -m venv venv
- source venv/bin/activate

4. Install requirements
- pip install -r requirements.txt

5. Apply migrations
- python manage.py makemigrations
- python manage.py migrate

6. Run server
- python manage.py runserver

7. Start front end
- Open index.html (for example with live server)

## Usage
1. Create a super user
- python manage.py createsuperuser

2. Create user
- Any further user you can either create in the django admin panel or directly in the front end.

## Testing
- python manage.py test

## Technologies
- JavaScript
- Python 3.11.5
- Django 5.1
- Django Rest Framework
