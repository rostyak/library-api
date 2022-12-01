import datetime


def get_expected_return_date(expected_days: int) -> datetime.date:
    current_date = datetime.date.today()
    return current_date + datetime.timedelta(days=expected_days)


def get_days_for_payment(start_date: datetime.date, end_date: datetime.date) -> int:
    difference = start_date - end_date
    return abs(difference.days)
