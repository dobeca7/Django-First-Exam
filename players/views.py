from academies.models import Academy
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from future_stars.mixins import AccountRequiredMixin
from players.forms import PlayerDeleteForm, PlayerForm
from players.models import Player


class PlayerCreateView(AccountRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = "players/player-form.html"
    success_url = reverse_lazy("player-list")
    success_message = "Player created successfully."
    permission_required = "players.add_player"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if request.user.role == "analyst":
            if not Academy.objects.exists():
                messages.warning(
                    request,
                    "A player cannot be created until at least one academy exists.",
                )
                return redirect("home")
            return super().dispatch(request, *args, **kwargs)

        if request.user.role == "academy_manager" and not request.user.owned_academies.exists():
            messages.warning(
                request,
                "Create an academy before adding players to your squad.",
            )
            return redirect("academy-create")

        if not request.user.owned_academies.exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class PlayerEditView(AccountRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = "players/player-form.html"
    success_url = reverse_lazy("player-list")
    permission_required = "players.change_player"

    def get_queryset(self):
        queryset = Player.objects.select_related("academy")
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(academy__owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


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


class PlayerDeleteView(AccountRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Player
    template_name = "players/player-confirm-delete.html"
    success_url = reverse_lazy("player-list")
    permission_required = "players.delete_player"

    def get_queryset(self):
        queryset = Player.objects.select_related("academy")
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(academy__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PlayerDeleteForm(instance=self.object)
        return context


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
