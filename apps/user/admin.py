from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user.models import *


# Register your models here.
class UserAdmin(BaseUserAdmin):

    list_display = ["id","email"]
    list_filter = ["is_active"]
    fieldsets = [
        (None, {"fields": ["email", "password", "created_at", "updated_at"]}),
        (
            "Personal info",
            {"fields": ["full_name"]}, 
        ),
        (
            "Permissions",
            {
                "fields": [
                  
                    "is_superuser",
                    "is_active",
                ]
            },
        ),
    ]

    search_fields = ["email"]

    ordering = ["-created_at"]

    readonly_fields = ["created_at", "updated_at"]


# Now register the new UserAdmin...
admin.site.register(UserModel, UserAdmin)