from rest_framework import generics
from rest_framework.permissions import AllowAny
from players.models import Player
from players.serializers import PlayerSerializer


class PlayerListApiView(generics.ListAPIView):
    queryset = Player.objects.select_related("academy").order_by("name")
    serializer_class = PlayerSerializer
    permission_classes = [AllowAny]
