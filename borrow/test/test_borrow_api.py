import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from borrow.models import Borrowing
from borrow.serializers import BorrowingListSerializer
from library.models import Book

BORROWING_URL = reverse("borrow:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrow:borrowing-detail", args=[borrowing_id])


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def sample_book(self, **params):
        defaults = {
            "title": "Sample movie",
            "authors": "Sample authors",
            "cover": "S",
            "inventory": 1,
            "daily_fee": "00.11"
        }
        defaults.update(params)

        return Book.objects.create(**defaults)

    def sample_borrowing(self, **params):
        defaults = {
            "book": self.sample_book(),
            "user": self.user
        }
        defaults.update(params)

        return Borrowing.objects.create(**defaults)

    def setUp(self):
        self.client = APIClient()
        self.admin = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.superuser = get_user_model().objects.create_superuser(
            "admin@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.admin.force_authenticate(self.superuser)

    def test_list_borrowings(self):
        self.sample_borrowing()
        self.sample_borrowing()

        res = self.client.get(BORROWING_URL)

        movies = Borrowing.objects.all().order_by("id")
        serializer = BorrowingListSerializer(movies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_active_borrowing(self):
        borrowing1 = self.sample_borrowing()
        borrowing2 = self.sample_borrowing()
        borrowing3 = self.sample_borrowing()

        borrowing1.actual_return_date = datetime.date.today()
        borrowing1.save()

        res = self.client.get(
            BORROWING_URL, {"is_active": True}
        )

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)
        serializer3 = BorrowingListSerializer(borrowing3)

        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)

    def test_borrowing_filter_by_user_if_admin(self):
        borrowing1 = self.sample_borrowing()
        borrowing2 = self.sample_borrowing()

        res = self.admin.get(
            BORROWING_URL, {"user_id": "2"}
        )

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)

        self.assertNotIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_borrowing_filter_by_user_if_user(self):
        borrowing1 = self.sample_borrowing()
        borrowing2 = self.sample_borrowing()

        res = self.client.get(
            BORROWING_URL, {"user_id": "2"}
        )

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_delete_borrowing_not_allowed(self):
        borrowing = self.sample_borrowing()
        url = detail_url(borrowing.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
