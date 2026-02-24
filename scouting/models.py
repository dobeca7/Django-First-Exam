from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from future_stars.models import TimeStampedModel
from scouting.choices import PlayerSkills, RecommendationChoices

class Skill(models.Model):

    name = models.CharField(max_length=50, unique=True)
    skill = models.CharField(
        max_length=50,
        choices=PlayerSkills,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class ScoutReport(TimeStampedModel):

    player = models.ForeignKey("players.Player", on_delete=models.CASCADE, related_name="reports")

    scout_name = models.CharField(max_length=60)

    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    skills = models.ManyToManyField("scouting.Skill", related_name="reports", blank=True)

    notes = models.TextField(max_length=300, blank=True)

    recommendation = models.CharField(
        max_length=10,
        choices=RecommendationChoices,
        default="monitor",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.player.name} - {self.rating}"
