from django.urls import path

from players.views import PlayerCreateView, PlayerDeleteView, PlayerDetailView, PlayerEditView, PlayerListView

urlpatterns = [
    path("", PlayerListView.as_view(), name="player-list"),
    path("create/", PlayerCreateView.as_view(), name="player-create"),
    path("<int:pk>/", PlayerDetailView.as_view(), name="player-detail"),
    path("<int:pk>/edit/", PlayerEditView.as_view(), name="player-edit"),
    path("<int:pk>/delete/", PlayerDeleteView.as_view(), name="player-delete"),
]
