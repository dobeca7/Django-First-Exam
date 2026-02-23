from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from players.forms import PlayerForm
from players.models import Player


def home(request):
    return render(request, "home.html")


class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = "players/player-form.html"
    success_url = reverse_lazy("player-list")


class PlayerEditView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = "players/player-form.html"
    success_url = reverse_lazy("player-list")


class PlayerListView(ListView):
    model = Player
    template_name = "players/player-list.html"
    context_object_name = "players"
    queryset = Player.objects.select_related("academy").order_by("-potential", "name")


class PlayerDetailView(DetailView):
    model = Player
    template_name = "players/player-detail.html"
    context_object_name = "player"


class PlayerDeleteView(DeleteView):
    model = Player
    template_name = "players/player-confirm-delete.html"
    success_url = reverse_lazy("player-list")
