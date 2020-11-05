import datetime
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.test import TestCase

from besttickets.settings import REST_FRAMEWORK
from tickets.models import Event
from tickets.serializers import EventSerializer


class EventModelTest(TestCase):
    def test_create_event(self):
        date_to_mock = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):
            event = Event(
                name="Best concert at National Stadium",
                date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
            )
            event.save()
            event.full_clean()
        self.assertEqual(event.name, "Best concert at National Stadium")
        self.assertEqual(
            event.date_event, datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc)
        )
        self.assertEqual(event.created_at, date_to_mock)

    def test_event_has_all_fields(self):
        event = Event(
            id=1,
            name="Best concert at National Stadium",
            date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
        )
        event.save()
        event.full_clean()

        self.assertEqual(event.id, 1)
        self.assertTrue(isinstance(event.name, str))
        self.assertTrue(isinstance(event.date_event, datetime.date))
        self.assertTrue(isinstance(event.created_at, datetime.date))

    def test_too_short_event_name(self):
        event = Event(
            name="K" * 4,
            date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
        )
        with self.assertRaises(ValidationError):
            event.save()
            event.full_clean()

    def test_too_long_event_name(self):
        event = Event(
            name="K" * 301,
            date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
        )
        with self.assertRaises(DataError):
            event.save()
            event.full_clean()

    def test_allow_duplicates_events(self):
        event = Event(
            name="Best concert at National Stadium",
            date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
        )
        event.save()
        event.full_clean()

        event_sec = Event(
            name="Best concert at National Stadium",
            date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
        )
        event_sec.save()
        event_sec.full_clean()  # should not raise a Validation error

        self.assertNotEqual(event, event_sec)
        self.assertEqual(event.name, event_sec.name)


class EventSerializerTest(TestCase):
    def setUp(self) -> None:
        self.event_attr = {
            "id": 1,
            "name": "Best concert at National Stadium",
            "date_event": datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc),
        }
        self.event_serialized = {
            "id": 1,
            "name": "Best concert at National Stadium",
            "date_event": datetime.datetime(
                2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc
            ).strftime(REST_FRAMEWORK["DATETIME_FORMAT"]),
        }
        self.event = Event.objects.create(**self.event_attr)
        self.serializer = EventSerializer(instance=self.event)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["id", "name", "date_event"])

    def test_contains_correct_data(self):
        self.assertEqual(self.serializer.data, self.event_serialized)

    def test_nested_serializer_without_tickets(self):
        data = self.serializer.data
        self.assertNotIn("tickets", data.keys())

    def test_nested_serializer_with_tickets(self):
        data = self.serializer.data
        self.assertNotIn("tickets", data.keys())

    # todo add serializer validation


class EventSerializerNestedTest(TestCase):
    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    def test_nested_serializer_with_tickets(self):
        event = Event.objects.get(pk=2)

        event_serializer = EventSerializer(event, nested=True)

        self.assertIn("ticket_types", event_serializer.data.keys())
