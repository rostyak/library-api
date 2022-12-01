from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentDetailSerializer,
    PaymentCreateSerializer,
)


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Payment.objects.select_related("borrowing")
        if self.request.user.is_staff:
            return queryset
        queryset = queryset.filter(borrowing__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        if self.action == "create":
            return PaymentCreateSerializer
        if self.action == "list":
            return PaymentCreateSerializer
        return PaymentSerializer
