from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from scouting.forms import ScoutReportForm
from scouting.models import ScoutReport


class ScoutReportCreateView(SuccessMessageMixin, CreateView):
    model = ScoutReport
    form_class = ScoutReportForm
    template_name = "scouting/scoutreport-form.html"
    success_url = reverse_lazy("report-list")
    success_message = "Scout report created successfully."


class ScoutReportEditView(UpdateView):
    model = ScoutReport
    form_class = ScoutReportForm
    template_name = "scouting/scoutreport-form.html"
    success_url = reverse_lazy("report-list")


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


class ScoutReportDeleteView(DeleteView):
    model = ScoutReport
    template_name = "scouting/scoutreport-confirm-delete.html"
    success_url = reverse_lazy("report-list")
