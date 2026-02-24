from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
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
        if (self.position == Player.PositionChoices.GOALKEEPER
                and self.dominant_foot == Player.DominantFootChoices.BOTH):
            raise ValidationError(
                {"dominant_foot": "The goalkeeper cannot have both dominant feet"}
            )

    def __str__(self):
        return f"{self.name} - {self.position}"
