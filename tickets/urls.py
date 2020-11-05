from django.urls import include, path
from rest_framework import routers

from tickets.views import (
    EventViewSet,
    OrderListView,
    TicketTypeDetailView,
    TicketTypeListView,
)

router = routers.DefaultRouter()
router.register(r"events", EventViewSet, basename="events")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "events/<int:event_id>/tickets/",
        TicketTypeListView.as_view(),
        name="tickets-type-for-event-list",
    ),
    path(
        "tickets/<int:ticket_type_id>/",
        TicketTypeDetailView.as_view(),
        name="ticket-type-detail",
    ),
    path("orders/", OrderListView.as_view(), name="order-list"),
]
