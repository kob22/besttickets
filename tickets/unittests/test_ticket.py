import datetime
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase

from tickets.models import Event, Ticket
from tickets.serializers import TicketSerializer


class TicketModelTest(TestCase):

    fixtures = ["tickets/unittests/fixtures/events.json"]

    def test_create_ticket(self):
        event = Event.objects.get(id=1)
        date_to_mock = datetime.datetime(2020, 2, 5, 22, 23, 1, tzinfo=pytz.utc)
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):
            ticket = Ticket(event=event, category="VIP", price=2000, qty=500)
            ticket.save()
            ticket.full_clean()
        self.assertEqual(ticket.event, event)
        self.assertEqual(ticket.created_at, date_to_mock)
        self.assertEqual(ticket.category, "VIP")
        self.assertEqual(ticket.price, 2000)
        self.assertEqual(ticket.qty, 500)

    def test_create_ticket_without_event(self):
        ticket = Ticket(category="VIP", price=2000, qty=500)

        with self.assertRaises(IntegrityError):
            ticket.save()
            ticket.full_clean()

    def test_create_ticket_with_non_event_object(self):

        with self.assertRaises(ValueError):
            ticket = Ticket(event=55, category="VIP", price=2000, qty=500)

    def test_max_length_category_field(self):
        event = Event.objects.get(id=1)
        with self.assertRaises(ValidationError):
            ticket = Ticket(event=event, category="V" * 51, price=2000, qty=500)
            ticket.save()
            ticket.full_clean()

    def test_delete_event_with_tickets_should_raise_error(self):
        event = Event.objects.get(id=1)

        ticket = Ticket(event=event, category="VIP", price=2000, qty=500)
        ticket.save()
        with self.assertRaises(ProtectedError):
            event.delete()


class TicketSerializerTest(TestCase):

    fixtures = ["tickets/unittests/fixtures/events.json"]

    def setUp(self) -> None:

        self.event = Event.objects.get(id=1)

        self.ticket_attr = {
            "event": self.event,
            "category": "Premium",
            "price": 3000,
            "qty": 99,
        }
        self.ticket_serialized = {
            "id": 1,
            "event": 1,
            "category": "Premium",
            "price": 3000,
            "qty": 99,
        }
        self.ticket = Ticket.objects.create(**self.ticket_attr)
        self.ticket_obj_serialized = TicketSerializer(instance=self.ticket)

    def test_ticket_serializer_contains_correct_data(self):
        self.assertEqual(self.ticket_obj_serialized.data, self.ticket_serialized)

    def test_create_ticket_from_data(self):
        self.serialized_ticket = TicketSerializer(data=self.ticket_serialized)
        self.assertTrue(self.serialized_ticket.is_valid())
