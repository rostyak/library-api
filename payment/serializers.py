from rest_framework import serializers

from borrow.serializers import BorrowingDetailSerializer
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status_payment",
            "type_payment",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )
        read_only_fields = ("id", "money_to_pay",)


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer()
