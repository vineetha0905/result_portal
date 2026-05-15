"""Django admin for cohort result PDFs — searchable changelist and clear upload fields."""

from django.contrib import admin
from django.db.models import Q

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """
    Upload **one** official PDF per pass-out year + academic year + semester.

    Use the search box on the changelist to quickly find existing publications
    (by year, semester label, or pass-out year digits).
    """

    list_display = (
        "pass_out_year",
        "academic_year",
        "semester",
        "upload_date",
        "pdf_file",
    )
    list_filter = ("pass_out_year", "academic_year", "semester")
    # Non-empty so the admin shows a search box; matching is implemented in
    # ``get_search_results`` (plain ``search_fields`` on integers is unreliable).
    search_fields = ("pass_out_year",)
    readonly_fields = ("upload_date",)
    ordering = ("-pass_out_year", "academic_year", "semester")
    list_per_page = 25

    fieldsets = (
        (
            None,
            {
                "fields": ("pass_out_year", "academic_year", "semester", "pdf_file"),
                "description": (
                    "Upload **one** official gazette PDF for this cohort and term. "
                    "Students in that pass-out year will see it on their dashboard; "
                    "they use Search in the PDF viewer to find their roll number."
                ),
            },
        ),
        ("Metadata", {"fields": ("upload_date",)}),
    )

    def get_search_results(self, request, queryset, search_term):
        """
        Match pass-out year (digits), academic year label (e.g. ``1st``), or semester text.
        """
        if not (search_term or "").strip():
            return queryset, False
        term = search_term.strip()
        q = Q()
        if term.isdigit():
            try:
                q |= Q(pass_out_year=int(term))
            except (TypeError, ValueError):
                pass
        t = term.lower()
        for val, label in Result.ACADEMIC_YEAR_CHOICES:
            if t in label.lower():
                q |= Q(academic_year=val)
        for val, label in Result.SEMESTER_CHOICES:
            if t in label.lower():
                q |= Q(semester=val)

        if not q:
            return queryset.none(), False
        return queryset.filter(q), False
