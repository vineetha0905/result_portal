# Data-preserving migration: per-student Result -> one cohort PDF per slot.

from django.conf import settings
from django.db import migrations, models


def forwards_copy_cohort_and_dedupe(apps, schema_editor):
    """Copy pass_out_year from linked student; keep one row per cohort slot."""
    Result = apps.get_model("results", "Result")
    Student = apps.get_model("accounts", "Student")

    for r in Result.objects.all():
        try:
            s = Student.objects.get(pk=r.student_id)
        except Student.DoesNotExist:
            r.pass_out_year = 2000
        else:
            r.pass_out_year = s.pass_out_year
        r.save(update_fields=["pass_out_year"])

    # Collapse duplicate (pass_out_year, academic_year, semester) after cohort move
    seen = set()
    for r in Result.objects.order_by("id"):
        key = (r.pass_out_year, r.academic_year, r.semester)
        if key in seen:
            r.delete()
        else:
            seen.add(key)


def backwards_noop(apps, schema_editor):
    """Cannot faithfully restore per-student rows."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("results", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="pass_out_year",
            field=models.PositiveIntegerField(
                help_text="Cohort / pass-out year this official result publication applies to.",
                null=True,
            ),
        ),
        migrations.RunPython(forwards_copy_cohort_and_dedupe, backwards_noop),
        migrations.AlterUniqueTogether(
            name="result",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="result",
            name="student",
        ),
        migrations.AlterField(
            model_name="result",
            name="pass_out_year",
            field=models.PositiveIntegerField(
                help_text="Cohort / pass-out year this official result publication applies to.",
            ),
        ),
        migrations.AlterField(
            model_name="result",
            name="pdf_file",
            field=models.FileField(
                help_text="Single official PDF for this cohort, academic year, and semester.",
                upload_to="results/%Y/",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="result",
            unique_together={("pass_out_year", "academic_year", "semester")},
        ),
        migrations.AlterModelOptions(
            name="result",
            options={
                "ordering": ["pass_out_year", "academic_year", "semester"],
                "verbose_name": "result",
                "verbose_name_plural": "results",
            },
        ),
    ]
