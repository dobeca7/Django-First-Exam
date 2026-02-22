from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from players.forms import PlayerCreateForm, PlayerEditForm
from players.models import Player


def home(request):
    return render(request, "home.html")


class PlayerListView(ListView):
    model = Player
    template_name = "players/player-list.html"
    context_object_name = "players"


class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerCreateForm
    template_name = "players/player-create.html"
    success_url = reverse_lazy("player-list")


class PlayerEditView(UpdateView):
    model = Player
    form_class = PlayerEditForm
    template_name = "players/player-edit.html"
    success_url = reverse_lazy("player-list")
