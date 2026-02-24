from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from future_stars.models import TimeStampedModel


class Academy(TimeStampedModel):

    name = models.CharField(max_length=100, unique=True)

    city = models.CharField(max_length=50)

    founded_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2100)]
    )

    slug = models.CharField(max_length=100,unique=True,blank=True,null=True)

    contact_email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.city})"
