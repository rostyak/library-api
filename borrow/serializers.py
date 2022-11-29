from rest_framework import serializers

from library.serializers import BookSerializer
from user.serializers import UserSerializer
from borrow.models import Borrowing, get_expected_return_date


class BorrowingSerializer(serializers.ModelSerializer):
    expected_days_to_return = serializers.IntegerField(min_value=1)

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
        extra_kwargs = {"expected_days_to_return": {"write_only": True}}

    def create(self, validated_data):
        return Borrowing.objects.create(
            expected_return_date=get_expected_return_date(
                validated_data["expected_days_to_return"]
            )
        )


class BorrowingListSerializer(BorrowingSerializer):
    pass


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
