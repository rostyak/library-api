import os
import requests

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
