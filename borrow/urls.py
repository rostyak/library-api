from django.urls import path, include
from rest_framework import routers

from borrow.views import BorrowingViewSet, BorrowingReturnView

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)
borrowing_return = BorrowingReturnView.as_view(actions={"put": "return"})

urlpatterns = [
    path("", include(router.urls)),
    path("borowings/<int: pk>/return", borrowing_return)
]

app_name = "borrow"
