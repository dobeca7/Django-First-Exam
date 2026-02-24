from django.db.models import Avg
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from players.forms import PlayerForm
from players.models import Player


class PlayerCreateView(SuccessMessageMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = "players/player-form.html"
    success_url = reverse_lazy("player-list")
    success_message = "Player created successfully."


class PlayerEditView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = "players/player-form.html"
    success_url = reverse_lazy("player-list")


class PlayerListView(ListView):
    model = Player
    template_name = "players/player-list.html"
    context_object_name = "players"
    paginate_by = 7
    queryset = (Player.objects.select_related("academy")
                .annotate(avg_report_rating=Avg("reports__rating"))
                .order_by("-potential", "name"))


class TopPlayerListView(ListView):
    model = Player
    template_name = "players/top-player-list.html"
    context_object_name = "players"
    paginate_by = 7
    queryset = (Player.objects.select_related("academy")
                .filter(potential__gt=90)
                .order_by("-potential", "name"))


class PlayerDetailView(DetailView):
    model = Player
    template_name = "players/player-detail.html"
    context_object_name = "player"


class PlayerDeleteView(DeleteView):
    model = Player
    template_name = "players/player-confirm-delete.html"
    success_url = reverse_lazy("player-list")


class ComparePlayersView(TemplateView):
    template_name = "players/player-compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_players = Player.objects.order_by("name")
        selected_ids_raw = self.request.GET.getlist("players")

        selected_ids = []
        for value in selected_ids_raw:
            if value.isdigit():
                selected_ids.append(int(value))

        selected_ids = list(dict.fromkeys(selected_ids))

        compare_error = None
        compared_players = Player.objects.none()

        if selected_ids:
            if len(selected_ids) < 2 or len(selected_ids) > 3:
                compare_error = "Please select exactly 2 or 3 players."
            else:
                compared_players_qs = (
                    Player.objects.select_related("academy")
                    .annotate(avg_report_rating=Avg("reports__rating"))
                    .filter(pk__in=selected_ids)
                )
                players_by_id = {player.pk: player for player in compared_players_qs}
                ordered_players = [players_by_id[player_id] for player_id in selected_ids if player_id in players_by_id]

                if len(ordered_players) < 2:
                    compare_error = "Please select valid players."
                else:
                    compared_players = ordered_players

        context["all_players"] = all_players
        context["selected_ids"] = selected_ids
        context["compared_players"] = compared_players
        context["compare_error"] = compare_error
        return context
