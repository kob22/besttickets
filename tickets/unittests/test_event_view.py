from django.test import TestCase
from rest_framework.test import APIRequestFactory
from tickets.views import EventViewSet
from tickets.models import Event
from tickets.serializers import EventSerializer
from django.urls import reverse
from rest_framework import status
import json
import datetime
import pytz
from unittest import mock


### There is only information about get event details in documentation, so tests are only for get views.


class EventViewsALLTest(TestCase):
    def test_get_all_events_empty_list(self):
        factory = APIRequestFactory()
        events_view = EventViewSet.as_view({"get": "list"})
        request = factory.get(reverse("events-list"))
        response = events_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])
        self.assertEqual(response["content-type"], "application/json")

    def test_get_all_events(self):
        date_to_mock = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        self.events_attr = [
            {
                "id": 1,
                "name": "Best concert at National Stadium",
                "date_event": datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
            },
            {
                "id": 2,
                "name": "Best concert in Gdansk",
                "date_event": datetime.datetime(2021, 11, 1, 18, 0, 0, tzinfo=pytz.utc),
            },
            {
                "id": 3,
                "name": "Best concert in Wroclaw",
                "date_event": datetime.datetime(2021, 8, 1, 18, 0, 0, tzinfo=pytz.utc),
            },
        ]
        self.events = []
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):
            for event in self.events_attr:
                self.events.append(Event.objects.create(**event))

        factory = APIRequestFactory()
        event_view = EventViewSet.as_view({"get": "list"})
        request = factory.get(reverse("events-list"))
        response = event_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content), EventSerializer(self.events, many=True).data
        )
        self.assertEqual(response["content-type"], "application/json")


class EventViewsDetailsTest(TestCase):
    def test_get_details_non_existing_event(self):
        factory = APIRequestFactory()
        event_view = EventViewSet.as_view({"get": "retrieve"})
        request = factory.get(reverse("events-detail", args=(1,)))
        response = event_view(request, pk=1)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})
        self.assertEqual(response["content-type"], "application/json")

    def test_get_details_single_event(self):
        date_to_mock = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        self.event_attr = {
            "id": 1,
            "name": "Best concert at National Stadium",
            "date_event": datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
        }

        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):
            self.event = Event.objects.create(**self.event_attr)

        factory = APIRequestFactory()
        event_view = EventViewSet.as_view({"get": "retrieve"})
        request = factory.get(reverse("events-detail", args=(1,)))
        response = event_view(request, pk=1)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), EventSerializer(self.event).data)
        self.assertEqual(response["content-type"], "application/json")
