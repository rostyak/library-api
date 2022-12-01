import datetime


def get_expected_return_date(expected_days: int) -> datetime:
    current_date = datetime.date.today()
    return current_date + datetime.timedelta(days=expected_days)


def get_days_for_payment(
        start_date: datetime,
        end_date: datetime
) -> int:
    difference = end_date - start_date
    return difference.days
