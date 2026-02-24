from django.urls import path

from players.views import (
    ComparePlayersView,
    PlayerCreateView,
    PlayerDeleteView,
    PlayerDetailView,
    PlayerEditView,
    PlayerListView,
    TopPlayerListView,
)

urlpatterns = [
    path("", PlayerListView.as_view(), name="player-list"),
    path("compare/", ComparePlayersView.as_view(), name="player-compare"),
    path("top/", TopPlayerListView.as_view(), name="player-top-list"),
    path("create/", PlayerCreateView.as_view(), name="player-create"),
    path("<int:pk>/", PlayerDetailView.as_view(), name="player-detail"),
    path("<int:pk>/edit/", PlayerEditView.as_view(), name="player-edit"),
    path("<int:pk>/delete/", PlayerDeleteView.as_view(), name="player-delete"),
]
