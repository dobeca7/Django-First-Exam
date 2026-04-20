from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from future_stars.mixins import AccountRequiredMixin
from scouting.forms import ScoutReportForm
from scouting.models import ScoutReport
from scouting.tasks import update_player_report_stats


class ScoutReportCreateView(AccountRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ScoutReport
    form_class = ScoutReportForm
    template_name = "scouting/scoutreport-form.html"
    success_url = reverse_lazy("report-list")
    success_message = "Scout report created successfully."
    permission_required = "scouting.add_scoutreport"

    def get_initial(self):
        initial = super().get_initial()
        player_id = self.request.GET.get("player")
        if player_id:
            initial["player"] = player_id
        return initial

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.owner = self.request.user
        response = super().form_valid(form)
        update_player_report_stats.delay(self.object.player_id)
        return response


class ScoutReportEditView(AccountRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ScoutReport
    form_class = ScoutReportForm
    template_name = "scouting/scoutreport-form.html"
    success_url = reverse_lazy("report-list")
    permission_required = "scouting.change_scoutreport"

    def get_queryset(self):
        queryset = ScoutReport.objects.select_related("player", "player__academy")
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        update_player_report_stats.delay(self.object.player_id)
        return response


class ScoutReportListView(ListView):
    model = ScoutReport
    template_name = "scouting/scoutreport-list.html"
    context_object_name = "reports"
    paginate_by = 7
    queryset = (
        ScoutReport.objects.select_related("player", "player__academy")
        .prefetch_related("skills")
        .order_by("-created_at")
    )


class ScoutReportDetailView(DetailView):
    model = ScoutReport
    template_name = "scouting/scoutreport-detail.html"
    context_object_name = "report"

    queryset = ScoutReport.objects.select_related("player", "player__academy").prefetch_related("skills")


class ScoutReportDeleteView(AccountRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ScoutReport
    template_name = "scouting/scoutreport-confirm-delete.html"
    success_url = reverse_lazy("report-list")
    permission_required = "scouting.delete_scoutreport"

    def get_queryset(self):
        queryset = ScoutReport.objects.select_related("player", "player__academy")
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)

    def form_valid(self, form):
        player_id = self.object.player_id
        response = super().form_valid(form)
        update_player_report_stats.delay(player_id)
        return response
