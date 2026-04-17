from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from scouting.models import ScoutReport
from scouting.serializers import ScoutReportSerializer


class ScoutReportListApiView(generics.ListAPIView):
    queryset = ScoutReport.objects.select_related("player").order_by("-created_at")
    serializer_class = ScoutReportSerializer
    permission_classes = [IsAuthenticated]
