from rest_framework import serializers

from players.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    academy_name = serializers.CharField(source="academy.name", read_only=True)

    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "birth_date",
            "nationality",
            "position",
            "dominant_foot",
            "potential",
            "academy",
            "academy_name",
        )
