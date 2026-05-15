"""
Custom user model: Student.

Students authenticate with ``registration_number`` (USERNAME_FIELD).
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import StudentManager


class Student(AbstractBaseUser, PermissionsMixin):
    """
    College student account.

    - ``registration_number``: unique login id (e.g. roll number).
    - ``pass_out_year``: used to filter which result PDFs this student sees.
    """

    name = models.CharField(max_length=120)
    registration_number = models.CharField(max_length=30, unique=True, db_index=True)
    pass_out_year = models.PositiveIntegerField(
        help_text="Graduation / pass-out year; results are matched to this year."
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into the admin site.",
    )

    objects = StudentManager()

    USERNAME_FIELD = "registration_number"
    REQUIRED_FIELDS = ["name", "pass_out_year"]

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"

    def __str__(self) -> str:
        return f"{self.registration_number} ({self.name})"

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name
