from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0003_remove_player_age_remove_player_skills_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="average_report_rating",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
        migrations.AddField(
            model_name="player",
            name="report_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
