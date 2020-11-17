import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIRequestFactory

from tickets.models import Event, TicketType
from tickets.serializers import TicketTypeSerializer
from tickets.views import TicketTypeListView, TicketTypeViewSet


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

        tickets_type_serialized = TicketTypeSerializer(
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
        ticket_type_view = TicketTypeViewSet.as_view({"get": "retrieve"})
        request = factory.get(reverse("ticket-types-detail", args=(222,)))
        response = ticket_type_view(request, pk=222)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})
        self.assertEqual(response["content-type"], "application/json")

    def test_get_existing_ticket_type(self):
        ticket_type_id = 3
        factory = APIRequestFactory()
        ticket_type_view = TicketTypeViewSet.as_view({"get": "retrieve"})
        request = factory.get(reverse("ticket-types-detail", args=(ticket_type_id,)))
        response = ticket_type_view(request, pk=ticket_type_id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.content,
            JSONRenderer().render(
                TicketTypeSerializer(TicketType.objects.get(pk=ticket_type_id)).data
            ),
        )
        self.assertEqual(response["content-type"], "application/json")


class TicketTypeViewsEmptyDB(TestCase):
    def test_get_all_ticket_type_empty_list(self):
        factory = APIRequestFactory()
        events_view = TicketTypeViewSet.as_view({"get": "list"})
        request = factory.get(reverse("ticket-types-list"))
        response = events_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])
        self.assertEqual(response["content-type"], "application/json")


class TicketTypeViewsWithTickets(TestCase):
    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    def test_get_all_tickets(self):
        factory = APIRequestFactory()
        events_view = TicketTypeViewSet.as_view({"get": "list"})
        request = factory.get(reverse("ticket-types-list"))
        response = events_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.content,
            JSONRenderer().render(
                TicketTypeSerializer(TicketType.objects.all(), many=True).data
            ),
        )
        self.assertEqual(response["content-type"], "application/json")


class TicketTypeViewsFilters(TestCase):
    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    def test_get_tickets_from_event_without_tickets(self):
        kwargs = {"event": 1}
        factory = APIRequestFactory()
        events_view = TicketTypeViewSet.as_view({"get": "list"})
        request = factory.get(reverse("ticket-types-list"), kwargs)
        response = events_view(request, kwargs)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), []),
        self.assertEqual(response["content-type"], "application/json")

    def test_get_tickets_from_event_with_tickets(self):
        kwargs = {"event": 2}
        factory = APIRequestFactory()
        events_view = TicketTypeViewSet.as_view({"get": "list"})
        request = factory.get(reverse("ticket-types-list"), kwargs)
        response = events_view(request, kwargs)
        response.render()

        event = Event.objects.get(pk=kwargs["event"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.content,
            JSONRenderer().render(
                TicketTypeSerializer(event.ticket_types, many=True).data
            ),
        ),
        self.assertEqual(response["content-type"], "application/json")

    def test_get_tickets_from_non_existing_event(self):
        kwargs = {"event": 222}
        factory = APIRequestFactory()
        events_view = TicketTypeViewSet.as_view({"get": "list"})
        request = factory.get(reverse("ticket-types-list"), kwargs)
        response = events_view(request, kwargs)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "event": [
                    "Select a valid choice. That choice is not one of the available choices."
                ]
            },
        ),
        self.assertEqual(response["content-type"], "application/json")
