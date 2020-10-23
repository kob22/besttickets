from django.test import TestCase
from django.core.exceptions import ValidationError
from tickets.models import Event
from tickets.serializers import EventSerializer
from besttickets.settings import REST_FRAMEWORK
import datetime

import pytz
from unittest import mock


class EventModelTest(TestCase):

    def test_create_event(self):
        date_to_mock = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=date_to_mock)):
            event = Event(name='Best concert at National Stadium', date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc))
            event.save()
            event.full_clean()
        self.assertEqual(event.name, 'Best concert at National Stadium')
        self.assertEqual(event.date_event, datetime.datetime(2021,10,1,18,0,0, tzinfo=pytz.utc))
        self.assertEqual(event.created_at, date_to_mock)

    def test_event_has_all_fields(self):
        event = Event(id=1, name='Best concert at National Stadium',
                      date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc))
        event.save()
        event.full_clean()

        self.assertEqual(event.id, 1)
        self.assertTrue(isinstance(event.name, str))
        self.assertTrue(isinstance(event.date_event, datetime.date))
        self.assertTrue(isinstance(event.created_at, datetime.date))

    def test_too_short_event_name(self):
        event = Event(name='K'*4,
                      date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc))
        with self.assertRaises(ValidationError):
            event.save()
            event.full_clean()

    def test_too_long_event_name(self):
        event = Event(name='K'*301,
                      date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc))
        with self.assertRaises(ValidationError):
            event.save()
            event.full_clean()

    def test_allow_duplicates_events(self):
        event = Event(name='Best concert at National Stadium',
                      date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc))
        event.save()
        event.full_clean()

        event_sec = Event(name='Best concert at National Stadium',
                      date_event=datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc))
        event_sec.save()
        event_sec.full_clean() # should not raise a Validation error

        self.assertNotEqual(event, event_sec)
        self.assertEqual(event.name, event_sec.name)


class EventSerializerTest(TestCase):

    def setUp(self) -> None:
        self.event_attr = {'id': 1, 'name': 'Best concert at National Stadium', 'date_event': datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc)}
        self.event_serialized = {'id': 1, 'name': 'Best concert at National Stadium', 'date_event': datetime.datetime(2021, 10, 1, 18, 0, 0, tzinfo=pytz.utc).strftime(REST_FRAMEWORK['DATETIME_FORMAT'])}
        self.event = Event.objects.create(**self.event_attr)
        self.serializer = EventSerializer(instance=self.event)

    def test_contains_expected_fields(self):

        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'date_event'])

    def test_contains_correct_data(self):
        self.assertEqual(self.serializer.data, self.event_serialized)