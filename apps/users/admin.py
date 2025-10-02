from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.actions import deactivate_users
from apps.users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "phone_number",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_deleted"
    )
    list_display_links = ("id", "phone_number")
    list_filter = ("is_staff", )
    search_fields = (
        "id",
        "phone_number",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("id",)
    actions = [deactivate_users]

    fieldsets = (
        (None, {"fields": ("phone_number", "username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_confirmed",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "username", "password1", "password2"),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )

