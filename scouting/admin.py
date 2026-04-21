from django.contrib import admin
from scouting.models import ScoutReport


@admin.register(ScoutReport)
class ScoutReportAdmin(admin.ModelAdmin):
    list_display = ("player", "scout_name", "rating", "recommendation", "owner", "created_at")
    list_filter = ("recommendation", "rating", "created_at")
    search_fields = ("player__name", "scout_name", "owner__username")
    filter_horizontal = ("skills",)
