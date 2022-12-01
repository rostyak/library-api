import datetime
import os
import requests

from borrow.models import Borrowing

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_message(borrowing):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?"

    message = (f"Created new borrowing!\n"
               f"Book: {borrowing.book}\n"
               f"Borrow date: {borrowing.borrow_date}\n"
               f"Expected return date: {borrowing.expected_return_date}")

    data = {'chat_id': CHAT_ID, 'text': message}

    requests.post(url, data)


def message_sent(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?"
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.get(url, data)
    return response.status_code


def send_overdue_message():
    overdue_limit = datetime.date.today() + datetime.timedelta(days=1)
    borrowings_filter = Borrowing.objects.filter(
        actual_return_date__isnull=True, expected_return_date__lte=overdue_limit
    ).select_related("book")

    if not borrowings_filter.exists():
        message_sent("No borrowings overdue today!")
        return

    for borrowing in borrowings_filter:
        user = borrowing.user
        message = (
            f"User {user.email} has an overdue borrowing:\n"
            f"Borrowing id: {borrowing.id}\n"
            f"Book name: “{borrowing.book}”, {borrowing.book.authors}\n"
            f"Borrow Date: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}")
        message_sent(message)
