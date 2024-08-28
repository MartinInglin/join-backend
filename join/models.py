from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="user",
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
        'Team',
        related_name="all_members",
        blank=True,
        help_text="The teams this user belongs to."
    )


class Team(models.Model):
    owner = models.ForeignKey(User, related_name='owned_teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members_team')
