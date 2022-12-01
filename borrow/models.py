from django.conf import settings
from django.db import models

from library_api.shortcuts import get_expected_return_date


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        null=True,
        default=get_expected_return_date(
            expected_days=settings.EXPECTED_DAYS_TO_RETURN
        ),
    )
    days_to_return = models.IntegerField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey("library.Book", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return (
            f"Borrowed at: {self.borrow_date}. "
            f"Expected to return: {self.expected_return_date}"
        )
