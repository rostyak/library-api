import stripe
from django.conf import settings
from rest_framework import serializers

from borrow.serializers import BorrowingDetailSerializer
from library_api.shortcuts import get_days_for_payment
from payment.models import Payment


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status_payment",
            "type_payment",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status_payment",
            "type_payment",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )
        read_only_fields = ("session_url", "session_id", "money_to_pay")


class PaymentCreateSerializer(PaymentListSerializer):
    def create(self, validated_data):
        status_payment = validated_data["status_payment"]
        type_payment = validated_data["type_payment"]
        borrowing = validated_data["borrowing"]

        start_date = borrowing.borrow_date
        end_date = borrowing.actual_return_date

        money_to_pay = get_days_for_payment(end_date, start_date) * float(
            borrowing.book.daily_fee
        )
        print(money_to_pay)

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": borrowing.book.title,
                        },
                        "unit_amount": money_to_pay,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://127.0.0.1:8000/api/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/api/cancel",
        )
        return Payment.objects.create(
            status_payment=status_payment,
            type_payment=type_payment,
            borrowing=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=money_to_pay,
        )


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer()
