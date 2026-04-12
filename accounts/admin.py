from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import AppUserAdminChangeForm, AppUserCreationForm
from accounts.models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = AppUserAdminChangeForm
    model = AppUser
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Football Profile", {"fields": ("role", "favorite_position", "bio")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Football Profile", {"fields": ("first_name", "last_name", "email", "role", "favorite_position", "bio")}),
    )
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
