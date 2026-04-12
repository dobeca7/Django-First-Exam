from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from scouting.forms import ScoutReportForm
from scouting.models import ScoutReport


class ScoutReportCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ScoutReport
    form_class = ScoutReportForm
    template_name = "scouting/scoutreport-form.html"
    success_url = reverse_lazy("report-list")
    success_message = "Scout report created successfully."
    permission_required = "scouting.add_scoutreport"


class ScoutReportEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ScoutReport
    form_class = ScoutReportForm
    template_name = "scouting/scoutreport-form.html"
    success_url = reverse_lazy("report-list")
    permission_required = "scouting.change_scoutreport"


class ScoutReportListView(ListView):
    model = ScoutReport
    template_name = "scouting/scoutreport-list.html"
    context_object_name = "reports"
    paginate_by = 7
    queryset = ScoutReport.objects.select_related("player", "player__academy").order_by("-created_at")


class ScoutReportDetailView(DetailView):
    model = ScoutReport
    template_name = "scouting/scoutreport-detail.html"
    context_object_name = "report"


class ScoutReportDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ScoutReport
    template_name = "scouting/scoutreport-confirm-delete.html"
    success_url = reverse_lazy("report-list")
    permission_required = "scouting.delete_scoutreport"
