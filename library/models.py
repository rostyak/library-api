from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    COVER_CHOICES = (("S", "soft"), ("H", "hard"))

    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)

    cover = models.CharField(
        max_length=255,
        choices=COVER_CHOICES
    )

    inventory = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
