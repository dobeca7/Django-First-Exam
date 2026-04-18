from celery import shared_task
from django.db.models import Avg, Count

from players.models import Player


@shared_task
def update_player_report_stats(player_id):
    player = Player.objects.filter(pk=player_id).first()
    if player is None:
        return

    stats = player.reports.aggregate(
        average_rating=Avg("rating"),
        total_reports=Count("id"),
    )
    player.average_report_rating = round(stats["average_rating"] or 0, 2)
    player.report_count = stats["total_reports"] or 0
    player.save(update_fields=["average_report_rating", "report_count", "updated_at"])
