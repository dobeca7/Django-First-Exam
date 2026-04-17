from rest_framework import serializers

from scouting.models import ScoutReport


class ScoutReportSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source="player.name", read_only=True)

    class Meta:
        model = ScoutReport
        fields = (
            "id",
            "player",
            "player_name",
            "scout_name",
            "rating",
            "recommendation",
            "notes",
            "created_at",
        )
