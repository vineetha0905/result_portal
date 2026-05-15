"""Student dashboard and PDF viewer views — cohort-scoped access control."""

from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Result


@login_required
def dashboard_view(request):
    """
    Show academic years and semesters for the logged-in student's cohort only.

    Identity comes from the authenticated session (registration number is the
    login id). Results are matched on ``pass_out_year`` so each student only
    sees publications for their own batch — not other cohorts' PDFs.
    """
    user = request.user
    cohort_year = user.pass_out_year
    results = Result.objects.filter(pass_out_year=cohort_year)

    grouped = defaultdict(list)
    for r in results.order_by("academic_year", "semester"):
        grouped[r.academic_year].append(r)

    academic_years = [
        {"code": code, "label": label, "results": grouped.get(code, [])}
        for code, label in Result.ACADEMIC_YEAR_CHOICES
    ]

    return render(
        request,
        "results/dashboard.html",
        {
            "academic_years": academic_years,
            "pass_out_year": cohort_year,
            "registration_number": user.registration_number,
        },
    )


@login_required
def view_pdf_view(request, result_id):
    """
    Open the PDF viewer only if this publication belongs to the student's cohort.

    Prevents students from guessing another result's primary key and viewing
    another cohort's file (object-level authorization).
    """
    user = request.user
    result = get_object_or_404(
        Result,
        pk=result_id,
        pass_out_year=user.pass_out_year,
    )

    pdf_url = result.pdf_file.url
    return render(
        request,
        "results/view_pdf.html",
        {
            "result": result,
            "pdf_url": pdf_url,
            "student_registration": user.registration_number,
        },
    )
