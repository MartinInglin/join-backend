from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text="Specific permissions for this user.",
    )

    user_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text="A hex code representing the user's color.",
    )

    phone_number = models.CharField(
        max_length=15, blank=True, null=True, help_text="The user's phone number."
    )

    teams = models.ManyToManyField(
        "Team",
        blank=True,
        help_text="The teams this user belongs to.",
    )


class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="team_members")


class Task(models.Model):
    PRIORITY_CHOICES = [
        (None, "No Priority"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("urgent", "Urgent"),
    ]
    CATEGORY_CHOICES = [
        ("technical_task", "Technical Task"),
        ("user_story", "User Story"),
    ]
    COLUMNS = [
        ("todo", "Todo"),
        ("in_progress", "In progress"),
        ("await_feedback", "Await feedback"),
        ("done", "Done")
    ]

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_author"
    )
    title = models.CharField(max_length=30)
    task = models.CharField(max_length=200, blank=True)
    assignedTo = models.ManyToManyField(User, related_name="task_members", blank=True)
    date = models.DateField(("Date"), blank=False, null=False)
    urgency = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True
    )
    category = models.CharField(
        max_length=15, choices=CATEGORY_CHOICES, blank=False, null=False
    )
    position = models.CharField(max_length=15, choices=COLUMNS, blank=False, null=False)
    subtasks = models.JSONField(default=list, blank=True)
