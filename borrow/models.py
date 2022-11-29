import datetime

from django.db import models


def get_expected_return_date(expected_days):
    current_date = datetime.date.today()
    return current_date + datetime.timedelta(days=expected_days)


class Borrow(models.Model):
    EXPECTED_DAYS_TO_RETURN = 10

    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        null=True,
        default=get_expected_return_date(
            expected_days=EXPECTED_DAYS_TO_RETURN
        ),
    )
    actual_return_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Borrowed at: {self.borrow_date}. Expected to return: {self.expected_return_date}"
