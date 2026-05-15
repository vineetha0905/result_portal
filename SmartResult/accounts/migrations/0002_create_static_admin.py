"""Create the built-in static admin account (username 'Admin', password 'admin').

This guarantees the project ships with working admin credentials so the
admin can immediately log in at /admin/ and start uploading PDFs.
"""

from django.db import migrations


ADMIN_REGISTRATION_NUMBER = "Admin"
ADMIN_PASSWORD = "admin"
ADMIN_NAME = "Portal Administrator"
ADMIN_PASS_OUT_YEAR = 2000


def create_static_admin(apps, schema_editor):
    """Create or refresh the 'Admin' superuser with the static password."""
    Student = apps.get_model("accounts", "Student")

    student, _created = Student.objects.get_or_create(
        registration_number=ADMIN_REGISTRATION_NUMBER,
        defaults={
            "name": ADMIN_NAME,
            "pass_out_year": ADMIN_PASS_OUT_YEAR,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )

    student.is_staff = True
    student.is_superuser = True
    student.is_active = True
    if not student.name:
        student.name = ADMIN_NAME
    if not student.pass_out_year:
        student.pass_out_year = ADMIN_PASS_OUT_YEAR

    from django.contrib.auth.hashers import make_password

    student.password = make_password(ADMIN_PASSWORD)
    student.save()


def remove_static_admin(apps, schema_editor):
    Student = apps.get_model("accounts", "Student")
    Student.objects.filter(registration_number=ADMIN_REGISTRATION_NUMBER).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_static_admin, remove_static_admin),
    ]
