"""Custom manager for Student user model."""

from django.contrib.auth.base_user import BaseUserManager


class StudentManager(BaseUserManager):
    """Creates and retrieves Student instances with normalized registration numbers."""

    def create_user(self, registration_number, password=None, **extra_fields):
        """Create and save a regular student with the given registration number and password."""
        if not registration_number:
            raise ValueError("Students must have a registration number")
        reg = str(registration_number).strip().upper()
        user = self.model(registration_number=reg, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, registration_number, password, **extra_fields):
        """Create and save a staff/superuser account (for Django admin)."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(registration_number, password, **extra_fields)
