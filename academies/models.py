from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Academy(models.Model):

    name = models.CharField(max_length=100, unique=True)

    city = models.CharField(max_length=50)

    founded_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2100)]
    )

    contact_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)


    def __str__(self):
        return f"{self.name} ({self.city})"
