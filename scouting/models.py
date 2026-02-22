from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Skill(models.Model):

    class PlayerSkills(models.TextChoices):
        FirstTouch = 'ft', 'First Touch'
        Dribbling = 'db' , 'Dribbling'
        Passing = 'ps' , 'Passing'
        Finishing = 'fn' , 'Finishing'
        BallControl = 'bc' , 'BallControl'
        Crossing = 'cr' , 'Crossing'
        SetPieces = 'sep' , 'SetPieces'
        Physical = 'ph' , 'Physical'
        Acceleration = 'ac' , 'Acceleration'
        SprintSpeed = 'sp' , 'SprintSpeed'
        Agility = 'ag' , 'Agility'
        Stamina = 'sta' , 'Stamina'
        Strength = 'st' , 'Strength'
        Balance = 'b' , 'Balance'
        Recovery = 'r' , 'Recovery'
        MentalStrength = 'mt' , 'MentalStrength'
        DecisionMaking = 'dm' , 'DecisionMaking'
        Concentration = 'c' , 'Concentration'
        Leadership = 'l' , 'Leadership'
        Confidence = 'con' , 'Confidence'
        Positioning = 'p' , 'Positioning'
        DefensiveAwareness = 'd' , 'DefensiveAwareness'
        GameReading = 'g' , 'GameReading'

    name = models.CharField(max_length=50, unique=True)
    skill = models.CharField(
        max_length=50,
        choices=PlayerSkills,
    )

    class Meta:
        ordering = ("name",)


    def __str__(self):
        return self.name


class ScoutReport(models.Model):

    class RecommendationChoices(models.TextChoices):
        SIGN = 'sign', 'Sign'
        MONITOR = 'monitor', 'Monitor'
        REJECT = 'reject', 'Reject'

    player = models.ForeignKey("players.Player", on_delete=models.CASCADE, related_name="reports")

    scout_name = models.CharField(max_length=60)

    report_date = models.DateField()

    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    skills = models.ManyToManyField("scouting.Skill", related_name="reports", blank=True)

    notes = models.TextField(max_length=300, blank=True)

    recommendation = models.CharField(
        max_length=10,
        choices=RecommendationChoices,
        default="monitor",
    )

    class Meta:
        ordering = ("-report_date",)

    def __str__(self):
        return f"{self.player.name} - {self.rating}"
