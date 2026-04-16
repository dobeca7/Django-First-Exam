from django.contrib import admin

from matches.models import Match, MatchParticipation


class MatchParticipationInline(admin.TabularInline):
    model = MatchParticipation
    extra = 1


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "home_academy",
        "away_academy",
        "date",
        "competition",
        "home_score",
        "away_score",
    )
    list_filter = ("competition", "date", "home_academy", "away_academy")
    search_fields = ("home_academy__name", "away_academy__name", "location", "competition")
    inlines = [MatchParticipationInline]


@admin.register(MatchParticipation)
class MatchParticipationAdmin(admin.ModelAdmin):
    list_display = ("match", "player", "started", "minutes_played", "goals", "assists")
    list_filter = ("started", "match__date")
    search_fields = ("player__name", "match__home_academy__name", "match__away_academy__name")
