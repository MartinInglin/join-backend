from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Team

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
    list_display = ('owner',)  # Customize fields displayed in the list view
    search_fields = ('owner__username', 'members__username')  # Allow searching by owner and members
    filter_horizontal = ('members',)  # Enable easier management of members in the team


# Register the customized UserAdmin
admin.site.register(User, UserAdmin)
