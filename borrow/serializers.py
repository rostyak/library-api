from rest_framework import serializers

from book.serializers import BookDetailSerializer
from user.serializers import UserDetailSerializer
from borrow.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )

class BorrowingListSerializer(BorrowingSerializer):
    pass

class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookDetailSerializer(many=False, read_only=True)
    user = UserDetailSerializer(many=False, read_only=True)

