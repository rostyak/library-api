import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrow.models import Borrowing
from borrow.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)
from notifications.notification import send_message


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

        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        created_borrowing = serializer.save(user=self.request.user)
        send_message(created_borrowing)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_staff",
                type={"type": "list", "items": {"type": "numbers"}},
                description="Filter by user id (example ?user_id=1)"
            ),
            OpenApiParameter(
                "is_active",
                type={"type": "list", "items": {"type": "numbers"}},
                description="Filter by book status (example ?is_active=True)"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return_borrowing",
        permission_classes=[IsAuthenticated],
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        print(request.data)

        if borrowing.actual_return_date:
            raise ValidationError("You can not return book twice")
        if borrowing.borrow_date > datetime.datetime.strptime(
                request.data.get("actual_return_date"), "%Y-%m-%d"
        ).date():
            raise ValidationError(
                {
                    "actual_return_date":
                    "Return date can not be earlier than borrow date"
                }
            )

        book = borrowing.book
        serializer = BorrowingReturnSerializer(borrowing, data=request.data)

        if serializer.is_valid():
            book.inventory += 1
            serializer.save()
            book.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
