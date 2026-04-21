from django.contrib import admin
from players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "academy", "position", "potential", "average_report_rating", "report_count")
    list_filter = ("position", "dominant_foot", "academy")
    search_fields = ("name", "nationality", "academy__name")
    readonly_fields = ("average_report_rating", "report_count")

    def get_fields(self, request, obj=None):
        fields = [
            "name",
            "birth_date",
            "nationality",
            "height",
            "weight",
            "position",
            "dominant_foot",
            "potential",
            "academy",
        ]
        if obj is not None:
            fields.extend(["average_report_rating", "report_count"])
        return fields
