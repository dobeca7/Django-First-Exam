from django.urls import path

from scouting.views import (
    ScoutReportCreateView,
    ScoutReportDeleteView,
    ScoutReportDetailView,
    ScoutReportEditView,
    ScoutReportListView,
)

urlpatterns = [
    path("", ScoutReportListView.as_view(), name="report-list"),
    path("create/", ScoutReportCreateView.as_view(), name="report-create"),
    path("<int:pk>/", ScoutReportDetailView.as_view(), name="report-detail"),
    path("<int:pk>/edit/", ScoutReportEditView.as_view(), name="report-edit"),
    path("<int:pk>/delete/", ScoutReportDeleteView.as_view(), name="report-delete"),
]
