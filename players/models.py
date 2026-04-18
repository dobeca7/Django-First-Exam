from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from datetime import date
from future_stars.models import TimeStampedModel


class Player(TimeStampedModel):

    class PositionChoices(models.TextChoices):
        GOALKEEPER = "GK", "Goalkeeper"
        DEFENDER = "DF", "Defender"
        MIDFIELDER = "MF", "Midfielder"
        FORWARD = "FW", "Forward"

    class DominantFootChoices(models.TextChoices):
        LEFT = "Left", 'Left'
        RIGHT = 'Right', 'Right'
        BOTH = 'Both', 'Both'

    name = models.CharField(max_length=100)

    birth_date = models.DateField()

    nationality = models.CharField(max_length=50)

    height = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(300)])

    weight = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(200)])

    position = models.CharField(
        max_length=10,
        choices=PositionChoices,
    )

    dominant_foot = models.CharField(max_length=10, choices=DominantFootChoices)

    potential = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    average_report_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    report_count = models.PositiveIntegerField(default=0)

    academy = models.ForeignKey("academies.Academy", on_delete=models.CASCADE, related_name="players")

    class Meta:
        ordering = ("-potential", "name")
        constraints = [
            models.UniqueConstraint(
                fields=["academy", "name", "birth_date"],
                name="unique_player",
            ),
        ]

    def clean(self):
        super().clean()
        if self.birth_date:
            min_birth_date = date(2000, 1, 1)
            max_birth_date = timezone.localdate()
            if not (min_birth_date <= self.birth_date <= max_birth_date):
                raise ValidationError(
                    {"birth_date": "Birth date must be between 01.01.2000 and today."}
                )
        if (self.position == Player.PositionChoices.GOALKEEPER
                and self.dominant_foot == Player.DominantFootChoices.BOTH):
            raise ValidationError(
                {"dominant_foot": "The goalkeeper cannot have both dominant feet"}
            )

    def __str__(self):
        return f"{self.name} - {self.position}"
