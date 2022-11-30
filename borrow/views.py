from rest_framework import mixins, viewsets, generics
from rest_framework.permissions import IsAuthenticated

from borrow.models import Borrowing
from borrow.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = self.queryset

            users = self.request.query_params.get("user_id")

            if users:
                users_ids = self._params_to_ints(users)
                queryset = queryset.filter(user__id__in=users_ids)

        else:
            queryset = Borrowing.objects.filter(user=self.request.user)

        is_active = self.request.query_params.get("is_active")

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BorrowingReturnView(mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = BorrowingReturnSerializer

    def borrowing_return(self, request, *args, **kwargs):
        pass