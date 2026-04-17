from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from matches.forms import MatchForm, MatchParticipationForm
from matches.models import Match, MatchParticipation


class MatchOwnerAccessMixin:
    def can_manage_match(self, match):
        user = self.request.user
        return user.is_superuser or match.home_academy.owner_id == user.id or match.away_academy.owner_id == user.id

    def get_managed_match(self):
        match = get_object_or_404(Match.objects.select_related("home_academy", "away_academy"), pk=self.kwargs["match_pk"])
        if not self.can_manage_match(match):
            raise PermissionDenied
        return match


class MatchCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Match
    form_class = MatchForm
    template_name = "matches/match-form.html"
    success_message = "Match created successfully."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.owned_academies.exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("match-detail", args=[self.object.pk])


class MatchEditView(LoginRequiredMixin, UpdateView):
    model = Match
    form_class = MatchForm
    template_name = "matches/match-form.html"

    def get_queryset(self):
        queryset = Match.objects.select_related("home_academy", "away_academy")
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(
            home_academy__owner=self.request.user
        ) | queryset.filter(
            away_academy__owner=self.request.user
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("match-detail", args=[self.object.pk])


class MatchListView(ListView):
    model = Match
    template_name = "matches/match-list.html"
    context_object_name = "matches"
    paginate_by = 7

    def get_queryset(self):
        return Match.objects.select_related("home_academy", "away_academy").order_by("date")


class MatchDetailView(DetailView):
    model = Match
    template_name = "matches/match-detail.html"
    context_object_name = "match"
    queryset = Match.objects.select_related("home_academy", "away_academy").prefetch_related(
        Prefetch(
            "participations",
            queryset=MatchParticipation.objects.select_related("player", "player__academy").order_by("-started", "-minutes_played", "player__name"),
        )
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_manage_match"] = user.is_authenticated and (
            user.is_superuser
            or self.object.home_academy.owner_id == user.id
            or self.object.away_academy.owner_id == user.id
        )
        return context


class MatchParticipationCreateView(LoginRequiredMixin, MatchOwnerAccessMixin, SuccessMessageMixin, CreateView):
    model = MatchParticipation
    form_class = MatchParticipationForm
    template_name = "matches/matchparticipation-form.html"
    success_message = "Player added to match successfully."

    def dispatch(self, request, *args, **kwargs):
        self.match = self.get_managed_match()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["match"] = self.match
        return kwargs

    def form_valid(self, form):
        form.instance.match = self.match
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("match-detail", args=[self.match.pk])


class MatchParticipationEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MatchParticipation
    form_class = MatchParticipationForm
    template_name = "matches/matchparticipation-form.html"
    success_message = "Match participation updated successfully."

    def get_queryset(self):
        queryset = MatchParticipation.objects.select_related(
            "match",
            "match__home_academy",
            "match__away_academy",
            "player",
        )
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(match__home_academy__owner=self.request.user) | queryset.filter(
            match__away_academy__owner=self.request.user
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["match"] = self.object.match
        return kwargs

    def get_success_url(self):
        return reverse("match-detail", args=[self.object.match_id])
