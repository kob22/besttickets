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

from tickets.views import EventViewSet, TicketDetailView, TicketListView

router = routers.DefaultRouter()
router.register(r"events", EventViewSet, basename="events")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "events/<int:event_id>/tickets/",
        TicketListView.as_view(),
        name="tickets-for-event-list",
    ),
    path("tickets/<int:ticket_id>/", TicketDetailView.as_view(), name="ticket-detail"),
]
