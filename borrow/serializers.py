import datetime

from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrow.shortcuts import get_expected_return_date
from library.serializers import BookSerializer
from user.serializers import UserSerializer
from borrow.models import Borrowing


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "days_to_return",
        )
        read_only_fields = (
            "expected_return_date",
            "actual_return_date",
        )
        extra_kwargs = {"days_to_return": {"write_only": True}}

    def validate(self, attrs):
        data = super(BorrowingCreateSerializer, self).validate(attrs=attrs)

        book = data["book"]
        if book.inventory < 1:
            raise ValidationError(
                {"inventory": "There must be books on shelf"}
            )

        return data

    def create(self, validated_data):
        with transaction.atomic():
            days_to_return = validated_data.pop("days_to_return")

            book = validated_data.pop("book")
            book.inventory -= 1
            book.save()
            book.refresh_from_db()
            validated_data["book"] = book

            borrowing = Borrowing.objects.create(**validated_data)

            if days_to_return:
                borrowing.expected_return_date = get_expected_return_date(
                    days_to_return
                )
                borrowing.save()

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
        read_only_fields = (
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
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
        read_only_fields = (
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)


class BorrowingReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date", "borrow_date")

    def validate(self, attrs):
        data = super(BorrowingReturnSerializer, self).validate(attrs=attrs)

        if data["actual_return_date"] > datetime.date.today():
            raise ValidationError(
                {
                    "actual_return_date":
                    "Actual return date con not be in future"
                }
            )

        return data
