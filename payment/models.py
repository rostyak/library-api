from django.db import models
from borrow.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = (("PE", "PENDING"), ("PA", "PAID"))
    TYPE_CHOICES = (("PA", "PAYMENT"), ("FI", "FINE"))

    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    status_payment = models.CharField(max_length=7, choices=STATUS_CHOICES)
    type_payment = models.CharField(max_length=7, choices=TYPE_CHOICES)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=5, decimal_places=2)
