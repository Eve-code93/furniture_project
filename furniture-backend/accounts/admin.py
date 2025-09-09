from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "email", "phone", "name", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser")
    search_fields = ("email", "phone", "name")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "phone", "name", "password")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "name", "password1", "password2", "role", "is_staff", "is_superuser"),
        }),
    )


admin.site.register(User, UserAdmin)
