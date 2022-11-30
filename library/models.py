from django.core.exceptions import ValidationError
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

    def clean(self):
        if self.inventory < 1:
            raise ValidationError(f"Ensure this value is greater "
                                  f"than or equal to 1.")

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        super(Book, self).save(
            force_insert, force_update, using, update_fields
        )
