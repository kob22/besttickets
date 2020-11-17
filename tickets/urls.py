from django.urls import include, path
from rest_framework import routers

from tickets.views import (
    EventViewSet,
    OrderListView,
    TicketTypeListView,
    TicketTypeViewSet,
)

router = routers.DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"ticket-types", TicketTypeViewSet, basename="ticket-types")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "events/<int:event_id>/tickets/",
        TicketTypeListView.as_view(),
        name="tickets-type-for-event-list",
    ),
    path("orders/", OrderListView.as_view(), name="order-list"),
]
