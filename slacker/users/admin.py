from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from slacker.users.forms import UserChangeForm, UserCreationForm
from slacker.users.models import User


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        ("Credentials", {"fields": (
            "id", "email", "name", "password", "creation_datetime",
        )}),
        ("Slack", {"fields": ("slack_user_id", "slack_workspace")}),

        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
    )
    readonly_fields = ("id", "creation_datetime",)
    list_display = ("id", "name", "slack_workspace", "email")
    list_filter = ("is_staff", "is_superuser",)
    search_fields = ("id", "email", "name")
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ('-creation_datetime',)
    raw_id_fields = ("slack_workspace", )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'name', 'password1', 'password2')
            }
        ),
    )


admin.site.register(User, UserAdmin)
