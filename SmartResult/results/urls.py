"""URL routes for dashboard and PDF viewer."""

from django.urls import path

from . import views

app_name = "results"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("result/<int:result_id>/view/", views.view_pdf_view, name="view_pdf"),
]
