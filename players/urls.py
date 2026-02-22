from django.urls import path

from players.views import PlayerCreateView, PlayerEditView, PlayerListView

urlpatterns = [
    path("", PlayerListView.as_view(), name="player-list"),
    path("create/", PlayerCreateView.as_view(), name="player-create"),
    path("<int:pk>/edit/", PlayerEditView.as_view(), name="player-edit"),
]
