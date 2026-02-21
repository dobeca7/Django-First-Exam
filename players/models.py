from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Player(models.Model):

    class PositionChoices(models.TextChoices):
        GOALKEEPER = "GK", "Goalkeeper"
        DEFENDER = "DF", "Defender"
        MIDFIELDER = "MF", "Midfielder"
        FORWARD = "FW", "Forward"

    class DominantFootChoices(models.TextChoices):
        LEFT = "left", 'left'
        RIGHT = 'right', 'right'
        BOTH = 'both', 'both'

    name = models.CharField(max_length=100)

    birth_date = models.DateField()

    age = models.PositiveIntegerField()

    position = models.CharField(
        max_length=10,
        choices=PositionChoices,
    )

    dominant_foot = models.CharField(max_length=10, choices=DominantFootChoices)

    potential = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    academy = models.ForeignKey("academies.Academy", on_delete=models.CASCADE, related_name="players")

    skills = models.ManyToManyField("scouting.Skill", related_name="players", blank=True)

    class Meta:
        ordering = ("-potential", "name")
        constraints = [
            models.UniqueConstraint(
                fields=["academy", "name", "birth_date"],
                name="unique_player",
            ),
        ]

    def clean(self):
        if self.position == "GOALKEEPER" and self.dominant_foot == "BOTH":
            raise ValidationError(
                {"goalkeeper": "The goalkeeper cannot have both dominant foots"}
            )
    def __str__(self):
        return f"{self.name} - {self.position}"
