from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "user_color",
        "phone_number",
        "is_staff",
    )
    
    # Add phone_number and user_color to fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('user_color', 'phone_number')}),
    )

# Register the customized UserAdmin
admin.site.register(User, UserAdmin)

