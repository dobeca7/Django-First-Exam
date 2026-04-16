from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from future_stars.models import TimeStampedModel


class Match(TimeStampedModel):
    home_academy = models.ForeignKey(
        "academies.Academy",
        on_delete=models.CASCADE,
        related_name="home_matches",
    )
    away_academy = models.ForeignKey(
        "academies.Academy",
        on_delete=models.CASCADE,
        related_name="away_matches",
    )
    players = models.ManyToManyField(
        "players.Player",
        through="MatchParticipation",
        related_name="matches",
    )
    date = models.DateField()
    location = models.CharField(max_length=100)
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    competition = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-date",)

    def clean(self):
        super().clean()
        if self.home_academy_id and self.home_academy_id == self.away_academy_id:
            raise ValidationError(
                {"away_academy": "The away academy must be different from the home academy."}
            )

    def __str__(self):
        return f"{self.home_academy} vs {self.away_academy}"


class MatchParticipation(TimeStampedModel):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="participations",
    )
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="match_participations",
    )
    started = models.BooleanField(default=False)
    minutes_played = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
    )
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("match", "player")
        constraints = [
            models.UniqueConstraint(
                fields=("match", "player"),
                name="unique_match_participation",
            ),
        ]

    def clean(self):
        super().clean()
        if self.match_id and self.player_id:
            valid_academy_ids = {
                self.match.home_academy_id,
                self.match.away_academy_id,
            }
            if self.player.academy_id not in valid_academy_ids:
                raise ValidationError(
                    {"player": "The player must belong to one of the two academies in the match."}
                )

    def __str__(self):
        return f"{self.player.name} in {self.match}"
