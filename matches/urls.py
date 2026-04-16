from django.urls import path

from matches.views import (
    MatchCreateView,
    MatchDetailView,
    MatchEditView,
    MatchListView,
    MatchParticipationCreateView,
    MatchParticipationEditView,
)


urlpatterns = [
    path("", MatchListView.as_view(), name="match-list"),
    path("create/", MatchCreateView.as_view(), name="match-create"),
    path("<int:pk>/", MatchDetailView.as_view(), name="match-detail"),
    path("<int:pk>/edit/", MatchEditView.as_view(), name="match-edit"),
    path("<int:match_pk>/participations/create/", MatchParticipationCreateView.as_view(), name="match-participation-create"),
    path("participations/<int:pk>/edit/", MatchParticipationEditView.as_view(), name="match-participation-edit"),
]
