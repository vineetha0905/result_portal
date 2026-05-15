"""Django admin registration for Student (custom user)."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Student


class StudentCreationForm(UserCreationForm):
    """Form for creating a new student from the admin site."""

    class Meta:
        model = Student
        fields = ("registration_number", "name", "pass_out_year")


class StudentChangeForm(UserChangeForm):
    """Form for editing an existing student in the admin site."""

    class Meta:
        model = Student
        fields = "__all__"


@admin.register(Student)
class StudentAdmin(BaseUserAdmin):
    """Admin UI for Student model (replaces default User admin)."""

    add_form = StudentCreationForm
    form = StudentChangeForm
    model = Student

    list_display = ("registration_number", "name", "pass_out_year", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "pass_out_year")
    search_fields = ("registration_number", "name")
    ordering = ("registration_number",)

    fieldsets = (
        (None, {"fields": ("registration_number", "password")}),
        ("Personal info", {"fields": ("name", "pass_out_year")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "registration_number",
                    "name",
                    "pass_out_year",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
