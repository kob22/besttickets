"""besttickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
