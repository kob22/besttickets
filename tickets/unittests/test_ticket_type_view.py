import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIRequestFactory

from tickets.models import TicketType
from tickets.serializers import TicketSerializer
from tickets.views import TicketTypeDetailView, TicketTypeListView


### There is only information about get tickets details in documentation, so tests are only for get views.
class TicketTypeViewsALLTest(TestCase):

    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    def test_get_all_tickets_type_from_event_no_tickets(self):
        factory = APIRequestFactory()
        tickets_type_view = TicketTypeListView.as_view()
        request = factory.get(reverse("tickets-type-for-event-list", args=(1,)))
        response = tickets_type_view(request, event_id=1)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])
        self.assertEqual(response["content-type"], "application/json")

    def test_get_all_tickets_type_from_wrong_id_event(self):
        factory = APIRequestFactory()
        tickets_type_view = TicketTypeListView.as_view()
        request = factory.get(reverse("tickets-type-for-event-list", args=(120,)))
        response = tickets_type_view(request, event_id=120)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})
        self.assertEqual(response["content-type"], "application/json")

    def test_get_all_tickets_type_from_event(self):
        event_id = 2
        factory = APIRequestFactory()
        tickets_type_view = TicketTypeListView.as_view()
        request = factory.get(reverse("tickets-type-for-event-list", args=(event_id,)))
        response = tickets_type_view(request, event_id=event_id)
        response.render()

        tickets_type_serialized = TicketSerializer(
            TicketType.objects.filter(event=event_id), many=True
        ).data
        tickets_type_json = JSONRenderer().render(tickets_type_serialized)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, tickets_type_json)
        self.assertEqual(response["content-type"], "application/json")


class TicketTypeViewsDetailTest(TestCase):

    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    def test_get_non_existing_tickets_type(self):
        factory = APIRequestFactory()
        ticket_type_view = TicketTypeDetailView.as_view()
        request = factory.get(reverse("ticket-type-detail", args=(222,)))
        response = ticket_type_view(request, ticket_type_id=222)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})
        self.assertEqual(response["content-type"], "application/json")

    def test_get_existing_ticket_type(self):
        ticket_type_id = 3
        factory = APIRequestFactory()
        ticket_type_view = TicketTypeDetailView.as_view()
        request = factory.get(reverse("ticket-type-detail", args=(ticket_type_id,)))
        response = ticket_type_view(request, ticket_type_id=ticket_type_id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.content,
            JSONRenderer().render(
                TicketSerializer(TicketType.objects.get(pk=ticket_type_id)).data
            ),
        )
        self.assertEqual(response["content-type"], "application/json")
