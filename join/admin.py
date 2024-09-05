from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Task, Team

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "is_staff",
        "id",
    )

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("user_color", "phone_number")}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("owner",)
    search_fields = ("owner__username", "members__username")
    filter_horizontal = ("members",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "id",
    )
    search_fields = ("author__username", "title")
    list_filter = ("urgency", "category", "position")
    filter_horizontal = ("assignedTo",)


admin.site.register(User, UserAdmin)
