from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentDetailSerializer,
    PaymentListSerializer,
    PaymentCreateSerializer,
)


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Payment.objects.select_related("borrowing")
        if self.request.user.is_staff:
            return queryset
        queryset = queryset.filter(borrowing__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        if self.action == "create":
            return PaymentCreateSerializer
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer
