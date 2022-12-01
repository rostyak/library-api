import datetime


def get_expected_return_date(expected_days):
    current_date = datetime.date.today()
    return current_date + datetime.timedelta(days=expected_days)
