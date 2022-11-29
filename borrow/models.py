import datetime

from django.conf import settings
from django.db import models


def get_expected_return_date(expected_days):
    current_date = datetime.date.today()
    return current_date + datetime.timedelta(days=expected_days)


class Borrowing(models.Model):
    EXPECTED_DAYS_TO_RETURN = 10

    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        null=True,
        default=get_expected_return_date(
            expected_days=EXPECTED_DAYS_TO_RETURN
        ),
    )
    days_to_return = models.IntegerField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey("library.Book", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Borrowed at: {self.borrow_date}. Expected to return: {self.expected_return_date}"
