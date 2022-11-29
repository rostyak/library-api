from rest_framework import serializers

from library.serializers import BookSerializer
from user.serializers import UserSerializer
from borrow.models import Borrowing, get_expected_return_date


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "days_to_return"
        )
        read_only_fields = ("expected_return_date",)
        extra_kwargs = {"days_to_return": {"write_only": True}}

    def create(self, validated_data):
        days_to_return = validated_data.pop("days_to_return")
        borrowing = Borrowing.objects.create(**validated_data)
        borrowing.expected_return_date = get_expected_return_date(days_to_return)
        return borrowing


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
    book_title = serializers.CharField(
        source="book.title", read_only=True
    )
    user_who_take = serializers.CharField(
        source="user.username", read_only=True
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "user_who_take",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
