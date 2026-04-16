from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from future_stars.models import TimeStampedModel


def validate_max_year(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError(f"Use a value between 1800 and {current_year}.")


class Academy(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_academies",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=100, unique=True)

    city = models.CharField(max_length=50)

    founded_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1800), validate_max_year]
    )

    slug = models.CharField(max_length=100,unique=True,blank=True,null=True)

    contact_email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.city})"
