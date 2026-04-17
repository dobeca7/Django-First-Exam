from django.urls import path

from players.api_views import PlayerListApiView
from scouting.api_views import ScoutReportListApiView


urlpatterns = [
    path("players/", PlayerListApiView.as_view(), name="api-player-list"),
    path("reports/", ScoutReportListApiView.as_view(), name="api-report-list"),
]
