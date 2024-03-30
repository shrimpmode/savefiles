from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import User
from django.utils.translation import gettext_lazy as _


class DeletedFilter(admin.SimpleListFilter):
    title = "Deleted"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return (
            ("deleted", "Deleted"),
            ("not_deleted", "Not Deleted"),
        )

    def queryset(self, request, queryset):
        if self.value() == "deleted":
            return User.deleted_objects.all()
        if self.value() == "not_deleted":
            return queryset


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name", "deleted_at", "is_deleted"]

    fieldsets = (
        (None, {"fields": ("email", "password", "deleted_at")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active",)}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                ),
            },
        ),
    )

    def is_deleted(self, obj):
        return obj.deleted_at is not None
    is_deleted.boolean = True
    is_deleted.short_description = 'Deleted?'

    list_filter = (DeletedFilter,)


admin.site.register(User, UserAdmin)
