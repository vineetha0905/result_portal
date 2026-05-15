"""Academic result PDF metadata — one official publication per cohort slot."""

from django.db import models


class Result(models.Model):
    """
    One published result PDF for a pass-out cohort, academic year, and semester.

    Admins upload a **single** official PDF per ``(pass_out_year, academic_year,
    semester)``. Students are identified by their **logged-in** account (roll /
    registration number). The dashboard only lists results where
    ``pass_out_year`` matches the student's profile, so they cannot open other
    cohorts' files. Within the PDF, students use the built-in search to locate
    their own row (standard practice for class-wide gazettes).
    """

    ACADEMIC_YEAR_CHOICES = [
        (1, "1st Year"),
        (2, "2nd Year"),
        (3, "3rd Year"),
        (4, "4th Year"),
    ]
    SEMESTER_CHOICES = [
        (1, "Semester 1"),
        (2, "Semester 2"),
    ]

    pass_out_year = models.PositiveIntegerField(
        help_text="Cohort / pass-out year this official result publication applies to.",
    )
    academic_year = models.PositiveSmallIntegerField(choices=ACADEMIC_YEAR_CHOICES)
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    pdf_file = models.FileField(
        upload_to="results/%Y/",
        help_text="Single official PDF for this cohort, academic year, and semester.",
    )
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "result"
        verbose_name_plural = "results"
        ordering = ["pass_out_year", "academic_year", "semester"]
        unique_together = ("pass_out_year", "academic_year", "semester")

    def __str__(self) -> str:
        return (
            f"{self.get_academic_year_display()} — "
            f"{self.get_semester_display()} "
            f"(pass-out {self.pass_out_year})"
        )
